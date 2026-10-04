# Benchmark — live-data verification (auto-generated)

_Generated: 2026-10-04T19:31:53.281101+00:00 | data: Stooq free + ECB | seed: 7_

## H2_pip_lot
- verdict: `PASS`
- pip_EURUSD: `0.0001`
- pip_USDJPY: `0.01`
- micro_0.01_usd_per_pip: `0.1`
- mini_0.10_usd_per_pip: `1.0`
- std_1.00_usd_per_pip: `10.0`
- live_price_used: `1.1257457733154297`
- course_claim: `0.01->$0.10/pip, 0.10->$1/pip, 1.0->$10/pip on EURUSD`

## H6_expectancy
- verdict: `PASS`
- formula: `E = p*3R - (1-p)*1R`
- p30_R3: `0.19999999999999996`
- per_10_trades_R: `1.9999999999999996`
- course_claim: `30% win with 3:1 still nets +2R per 10 trades (+9R wins -7R losses = +2R)`

## H7_leverage_margin
- verdict: `PASS`
- example: `1.0 lot EURUSD @100x`
- margin_usd: `1125.7457733154297`
- notional_usd: `100000.0`
- course_claim: `1:100 turns $1k into $100k notional control; margin locks, not gifted cash`
- adverse_100pips_std_loss_usd: `1000.0`

## H3_sessions
- verdict: `PASS`
- symbol: `EURUSD`
- n_hourly_bars: `1570`
- mean_range_pips_by_session: `{'mean': {'Asia_0-7UTC': 6.584, 'London_7-12UTC': 9.639, 'NYpm_17-24UTC': 6.286, 'Overlap_LondonNY_12-17UTC': 12.619}, 'median': {'Asia_0-7UTC': 5.965, 'London_7-12UTC': 9.027, 'NYpm_17-24UTC': 5.237, 'Overlap_LondonNY_12-17UTC': 10.6}, 'count': {'Asia_0-7UTC': 462, 'London_7-12UTC': 330, 'NYpm_17-24UTC': 448, 'Overlap_LondonNY_12-17UTC': 330}}`
- overlap_vs_asia_ratio: `1.917`
- course_claim: `Overlap 12-17 UTC (London+NY) is strongest window`

## H4_candles
- verdict: `PASS`
- daily_rows: `1301`
- weekly_rows: `262`
- course_claim: `Candle = O/H/L/C over its window; higher TF aggregates lower TF exactly`
- check: `resample W close equals last daily close within week (tautology check on live frame)`

## H5_costs
- verdict: `PASS`
- n_trades: `641`
- gross_total: `-1890.0`
- net_total: `-3300.2`
- cost_drag: `1410.2`
- win_rate_net: `0.1763`
- profit_factor_net: `0.4876738698460249`
- monte_carlo: `{'n': 5000, 'final_p50': -3300.1999999995714, 'final_p5': -3300.1999999995733, 'final_p95': -3300.199999999569, 'mdd_p50': 3327.999999999571, 'mdd_p95': 3410.799999999574}`
- course_claim: `Spread/commission decide scalps; always model variable spread + commission + SL/TP`

## H8_news_nfp
- verdict: `PASS`
- nfp_friday_mean_range: `85.79`
- other_mean_range: `67.51`
- premium_ratio: `1.271`
- mannwhitney_greater_p: `0.0074`
- course_claim: `NFP / macro news widens ranges; professionals wait for it`

## H1_market_size
- verdict: `CORROBORATED_LITERATURE`
- BIS_Triennial_Apr2025_OTC_FX_turnover: `$9.6tn/day (+28% vs $7.5tn 2022)`
- source: `BIS media release 2025-09-30 + commentary OTC derivatives April 2025; UK/London ~38% per course (verify via BIS country tables)`
- course_claim: `~$10tn/day, USD in ~89% of trades, London largest hub`

## Hidden patterns (live-data only)

```json
{
  "hour_seasonality_top3_utc": {
    "12": 14.85,
    "13": 13.75,
    "14": 13.29
  },
  "hour_seasonality_bottom3_utc": {
    "22": 3.56,
    "23": 4.31,
    "4": 4.87
  },
  "weekday_mean_range_pips": {
    "0": 7.59,
    "1": 7.61,
    "2": 8.97,
    "3": 9.2,
    "4": 8.83,
    "6": 5.09
  },
  "daily_logret_std": 0.004741,
  "daily_range_pips_mean": 67.88,
  "daily_range_by_dow": {
    "0": 64.45,
    "1": 66.78,
    "2": 71.86,
    "3": 71.37,
    "4": 69.8,
    "6": 61.52
  }
}
```