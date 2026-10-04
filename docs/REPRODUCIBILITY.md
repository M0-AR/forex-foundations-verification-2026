# Reproducibility

All claims in `README.md` are machine-generated from live public data.
No hand-edited numbers.

## One-command reproduction

```bash
docker compose up --build research
# or without docker:
make verify
# equivalent:
#   python3 src/data_fetch.py
#   PYTHONPATH=$PWD python3 experiments/09_full_benchmark.py
#   python3 -m pytest tests/ -q
```

## Determinism

- Seed `7` everywhere (`config/experiments.yaml`, Monte Carlo `n=5000`).
- UTC everywhere. Hourly bars carry `DateTime` UTC.
- No-lookahead: signal at close[t] fills at open[t+1]; SL-first pessimistic on same-bar SL+TP.
- Costs explicit: `spread_pips` + `commission_rt` per trade; swap reported separately.
- Manifests: every `data/*.csv` has `.manifest.json` with rows/sha/URL/UTC time.
- Outputs: `results/benchmark.json` (canonical), `results/benchmark.md` (render), `results/figures/*.png`.

## Data provenance (verified 2026-10-04, this host)

- Yahoo Finance v8, no key: `EURUSD=X, GBPUSD=X, JPY=X, CHF=X, AUDUSD=X, CAD=X, NZDUSD=X, GC=F (gold), BTC-USD`
  - daily `1d/5y`: ~1301 rows per FX pair (2021-10-03 → 2026-10-02), gold 1258, BTC 1827.
  - hourly `1h/3mo`: EURUSD 1570, GBPUSD 1570, USDJPY 1562, XAUUSD 1470 bars.
- Frankfurter (ECB): 1732 daily rows 2020-01-01 → 2026-10-02, EUR base.
- ECB 90-day XML: 65 rows (cross-check).
- Stooq CSV: blocked from server IP by JS challenge on 2026-10-04; retained as best-effort only.
  Documented here so others can reproduce with Stooq where reachable.

## QFRS-2026 alignment (seven standards)

1. Dataset construction — versioned manifests + fetch URLs.
2. Labelling — signals defined before seeing OOS; toy momentum labelled at close[t].
3. Point-in-time features — rolling SMA/returns shifted by one bar.
4. Leakage-free scaling — no scaling used; raw OHLC only.
5. Time-respecting splits — chronological backtest; walk-forward recommended for extensions.
6. Evaluation metrics — win rate, profit factor, expectancy, Sharpe proxy, Calmar-style MDD, Monte Carlo p50/p95.
7. Cost-aware backtest — spread + commission + SL/TP intrabar + max-hold timeout.

See `docs/METHODS.md` and `docs/LIVE_DATA.md`.
