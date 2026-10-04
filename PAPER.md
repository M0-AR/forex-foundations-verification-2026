# PAPER — submission-ready draft (companion to README)

See `README.md` for the full publishable paper (abstract → references, 8 hypotheses,
live-data tables, hidden patterns, roadmap). This file is the 2-page submission
cover so reviewers can triage in 5 minutes without losing provenance.

## Title

Verifying Retail Forex Foundations End-to-End on Live Public Data

## One-paragraph claim

Eight falsifiable hypotheses distilled from a 7-video Arabic retail-forex course
were tested keylessly on Yahoo/Frankfurter/ECB live data (2021–2026) under QFRS-2026
with a no-lookahead, cost-aware engine + 5,000-shuffle Monte Carlo. Result on
2026-10-04: **8/8 PASS/CORROBORATED**. Session premium **1.917×** (overlap
12.619 vs Asia 6.584 pips, n=1,570 hourly), NFP-day premium **1.271×
(p=0.0074)**, pip/lot and 30%×3:1 expectancy identities exact, margin math exact,
and an honest losing momentum baseline (gross −$1,890 → net −$3,300, drag
$1,410, n=641) proving cost modelling works. Hidden intraday peaks **12/13/14
UTC** (14.85/13.75/13.29 pips) vs troughs **22/23/04 UTC** define the PhD
follow-up.

## Artefacts

- `results/benchmark.json` (canonical) + `results/benchmark.md` + `results/figures/`
- `data/fetch_summary.json` + per-file manifests
- `docker-compose.yml` one-command reproduction; `make verify`

## Reproduction

```bash
docker compose up --build research
```

*Not financial advice. See README §6 Ethics.*
