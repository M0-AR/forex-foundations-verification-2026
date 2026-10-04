# Live-data notes

## What worked without keys (2026-10-04, this host)

| Source | URL pattern | Result |
|---|---|---|
| Yahoo daily | `query2.../chart/EURUSD=X?interval=1d&range=5y` | 1301 rows/pair, 2021-10-03 → 2026-10-02 |
| Yahoo hourly | `.../EURUSD=X?interval=1h&range=3mo` | 1570 (EURUSD), 1570 (GBPUSD), 1562 (USDJPY), 1470 (XAUUSD) |
| Frankfurter | `api.frankfurter.app/2020-01-01..?from=EUR&to=USD,GBP,JPY,CHF,AUD,CAD,NZD` | 1732 rows |
| ECB XML | `ecb.europa.eu/.../eurofxref-hist-90d.xml` | 65 rows |
| Stooq CSV | `stooq.com/q/d/l/?s=eurusd&i=d` | HTTP 200 but JS-challenge HTML, unusable server-side |

## Tickers

`EURUSD=X, GBPUSD=X, JPY=X, CHF=X, AUDUSD=X, CAD=X, NZDUSD=X, GC=F, BTC-USD`.

## Limitations

- Yahoo adjusts for splits/dividends on equities; FX spot has no adjustment issue, but weekend gaps exist (24/5 market). No interpolation is performed.
- Hourly history is last ~3 months only; session seasonality is therefore a recent-regime snapshot, re-run to refresh.
- Spreads are modelled (1.5 pips) not observed tick spreads; variable-spread extension needs Dukascopy/TrueFX tick data where reachable.
- Gold pip convention fixed at `0.1` per course; brokers vary (some quote 2 decimals). `pip_size("XAUUSD")` is explicit and tested.
