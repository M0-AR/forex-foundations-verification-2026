"""No-lookahead backtest primitives + cost-aware fill model.

Rules enforced (QFRS-aligned):
- signal at close[t] -> earliest fill at open[t+1]
- SL/TP resolved on bar t+1 high/low with pessimistic ordering (SL first)
- spread + commission + optional swap charged explicitly
- walk-forward + Monte Carlo live in experiments, not hidden here
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def apply_costs(gross: float, spread_pips: float, pip_value: float, commission_rt: float = 0.0, swap: float = 0.0) -> float:
    return float(gross - spread_pips * pip_value - commission_rt - swap)


def backtest_market_orders(
    df: pd.DataFrame,
    signals: pd.Series,  # +1 buy, -1 sell, 0 flat, indexed like df, computed from close[t] only
    symbol: str = "EURUSD",
    lot: float = 0.10,
    tp_pips: float = 30.0,
    sl_pips: float = 10.0,
    spread_pips: float = 1.5,
    commission_rt: float = 0.0,
    pip_size: float = 0.0001,
    max_hold_bars: int = 48,
) -> pd.DataFrame:
    """Bar-by-bar, no-lookahead. One position at a time. Returns trades dataframe."""
    from .fx_math import pip_value_per_lot_usd
    trades = []
    pos = None
    closes = df["Close"].to_numpy()
    highs = df["High"].to_numpy()
    lows = df["Low"].to_numpy()
    opens = df["Open"].to_numpy()
    sig = signals.to_numpy()
    times = df["Date"].to_numpy() if "Date" in df.columns else df.index.to_numpy()

    for t in range(len(df) - 1):
        if pos is None and sig[t] != 0:
            entry = float(opens[t + 1])
            pv = pip_value_per_lot_usd(symbol, lot, entry)
            pos = {"dir": int(np.sign(sig[t])), "entry": entry, "t_in": t + 1, "time_in": times[t + 1], "pv": pv}
        elif pos is not None:
            d = pos["dir"]
            # TP/SL levels
            tp = pos["entry"] + d * tp_pips * pip_size
            sl = pos["entry"] - d * sl_pips * pip_size
            h, low = float(highs[t]), float(lows[t])
            hit_tp = (h >= tp) if d == 1 else (low <= tp)
            hit_sl = (low <= sl) if d == 1 else (h >= sl)
            expired = (t - pos["t_in"]) >= max_hold_bars
            exit_px, reason = None, None
            if hit_sl and hit_tp:
                exit_px, reason = sl, "SL_first_pessimistic"
            elif hit_sl:
                exit_px, reason = sl, "SL"
            elif hit_tp:
                exit_px, reason = tp, "TP"
            elif expired:
                exit_px, reason = float(closes[t]), "TIME"
            if exit_px is not None:
                gross_pips = (exit_px - pos["entry"]) / pip_size * d
                gross = gross_pips * pos["pv"]
                net = apply_costs(gross, spread_pips, pos["pv"], commission_rt, 0.0)
                trades.append({
                    "dir": d, "entry": pos["entry"], "exit": exit_px, "lot": lot,
                    "gross_pips": gross_pips, "gross_usd": gross, "net_usd": net,
                    "reason": reason, "bars_held": t - pos["t_in"],
                    "time_in": pos["time_in"], "time_out": times[t],
                })
                pos = None
    return pd.DataFrame(trades)


def trade_stats(trades: pd.DataFrame) -> dict:
    if trades is None or len(trades) == 0:
        return {"n": 0}
    w = (trades["net_usd"] > 0).mean()
    pf_num = trades.loc[trades["net_usd"] > 0, "net_usd"].sum()
    pf_den = -trades.loc[trades["net_usd"] <= 0, "net_usd"].sum()
    pf = float(pf_num / pf_den) if pf_den > 0 else float("inf")
    rets = trades["net_usd"].to_numpy()
    sharpe = float(rets.mean() / (rets.std(ddof=1) + 1e-12) * (252 ** 0.5)) if len(rets) > 2 else 0.0
    return {
        "n": int(len(trades)),
        "win_rate": float(w),
        "profit_factor": float(pf),
        "expectancy_usd": float(rets.mean()),
        "total_net": float(rets.sum()),
        "sharpe_per_trade_annualized_proxy": float(sharpe),
        "max_loss": float(rets.min()),
        "max_win": float(rets.max()),
    }


def monte_carlo_shuffle(trades: pd.DataFrame, n: int = 5000, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    if trades is None or len(trades) == 0:
        return {"n": 0}
    v = trades["net_usd"].to_numpy()
    finals, mdds = [], []
    for _ in range(n):
        perm = rng.permutation(v)
        eq = np.cumsum(perm)
        peak = np.maximum.accumulate(np.concatenate([[0], eq]))
        dd = peak[1:] - eq
        finals.append(eq[-1])
        mdds.append(dd.max())
    finals = np.array(finals)
    mdds = np.array(mdds)
    return {
        "n": int(n),
        "final_p50": float(np.median(finals)),
        "final_p5": float(np.percentile(finals, 5)),
        "final_p95": float(np.percentile(finals, 95)),
        "mdd_p50": float(np.median(mdds)),
        "mdd_p95": float(np.percentile(mdds, 95)),
    }
