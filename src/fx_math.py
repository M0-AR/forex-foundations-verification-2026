"""Core forex math: pips, lots, margin, expectancy. Pure functions, unit-tested."""
from __future__ import annotations


def pip_size(symbol: str) -> float:
    s = symbol.upper()
    if "JPY" in s:
        return 0.01
    if s == "XAUUSD":
        return 0.1  # course convention: gold pip = 0.10 move; keep explicit
    return 0.0001


def pip_value_per_lot_usd(symbol: str, lot: float, price: float) -> float:
    """USD value of 1 pip for `lot` at `price`. Course rule: 0.01->10c, 0.10->$1, 1.0->$10 on EURUSD."""
    s = symbol.upper()
    if s == "XAUUSD":
        # 1.0 lot gold ~= $10 per $1 move => $1 per 0.1 (one gold-pip)
        return float(lot * 10.0)
    if "USD" in s and s.endswith("USD"):  # XXX/USD quote in USD
        return float(lot * 10.0)
    if s.startswith("USD"):  # USD/XXX: convert by price
        return float(lot * 10.0 / price) if price else 0.0
    # cross: approximate via price
    return float(lot * 10.0)


def pnl_usd(symbol: str, direction: int, entry: float, exit_: float, lot: float) -> float:
    """direction +1 buy, -1 sell."""
    ps = pip_size(symbol)
    pips = (exit_ - entry) / ps * direction
    return float(pips * pip_value_per_lot_usd(symbol, lot, entry))


def margin_required_usd(lot: float, contract_size: float, price: float, leverage: float) -> float:
    # standard FX: 1.0 lot = 100k base; gold 1.0 lot = 100 oz
    return float(lot * contract_size * price / leverage) if leverage else 0.0


def expectancy_per_trade(win_rate: float, avg_win: float, avg_loss: float) -> float:
    # avg_loss positive number; E = p*W - (1-p)*L
    return float(win_rate * avg_win - (1 - win_rate) * avg_loss)


def risk_of_ruin_approx(win_rate: float, rr: float) -> float:
    """Simple gambler's-ruin proxy with fixed fractional risk; rr = reward/risk multiple.
    Uses E>0 condition: ruin ~ ((1-p)/p * 1/rr concept). Kept as diagnostic, not theorem."""
    if win_rate <= 0:
        return 1.0
    if win_rate >= 1:
        return 0.0
    q, p = 1 - win_rate, win_rate
    # classic p-ruin for even-money scaled by rr edge factor
    edge = p * rr - q
    if edge <= 0:
        return 1.0
    return float(max(0.0, min(1.0, (q / p) ** (1 + rr))))
