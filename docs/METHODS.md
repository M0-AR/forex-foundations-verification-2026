# Methods

## Design

This repo tests the falsifiable core of a 7-video Arabic retail-forex course
(trading definition → forex structure → price drivers → candles → orders →
pips/lots → broker/costs → leverage/swap → risk psychology → MT5 practice)
as eight hypotheses H1–H8. Each maps to one course module and one experiment.

## No-lookahead engine (`src/backtest.py`)

- Input: OHLC dataframe + signal series `s[t] ∈ {+1,0,-1}` computed from `close[≤t]` only.
- Fill: `entry = open[t+1]`.
- SL/TP: resolved on bar `t` high/low; if both hit, SL first (pessimistic).
- Costs: `net = gross − spread_pips·pip_value − commission_RT − swap`.
- One position at a time, `max_hold_bars=48` timeout at close.
- Statistics: `trade_stats()` (n, win rate, profit factor, expectancy, Sharpe proxy).
- Robustness: `monte_carlo_shuffle(n=5000, seed=7)` reshuffles trade order;
  reports final-equity p50/p5/p95 and max-drawdown p50/p95.

## Session test (H3)

Hourly ranges in pips: `(High−Low)/pip_size`. Sessions in UTC:
Asia 0–7, London 7–12, Overlap 12–17, NY-pm 17–24. Compares mean/median;
verdict PASS iff `mean_overlap / mean_asia > 1.2`.

## News test (H8)

Daily ranges in pips. NFP proxy: first Friday of month (`weekday==4 & day<=7`).
Mann–Whitney U (greater) on NFP-Friday vs other days; PASS iff premium > 1
and `p < 0.10`. This is a volatility premium, not a directional edge.

## Cost test (H5)

Toy momentum (5-day return sign) on EURUSD daily with `30TP/10SL`,
`0.10 lot`, once with zero costs and once with `1.5 pips + $0.70 RT`
(`$7/lot RT × 0.10`). Reports `cost_drag = gross − net`. The toy is
intentionally naive: it demonstrates cost accounting and honest reporting
of a losing baseline (gross −$1890 → net −$3300 on this window).

## Expectancy (H6)

Analytic: `E = p·3R − (1−p)·1R`. At `p=0.30`, `E=+0.20R`/trade → `+2R`/10 trades.

## Walk-forward guidance

`09_full_benchmark.py` is the single-window baseline. For publication,
extend with rolling 6-mo-train/2-mo-test walk-forward and report stitched OOS
only, per 2026 best practice (TradeMetricsPro, FXVPS pipeline, Freqtrade docs,
DaruFinance WFO engine, QFRS-2026). The code is structured so `signals` can be
replaced without touching the fill engine.
