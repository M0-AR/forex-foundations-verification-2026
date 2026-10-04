"""Thin runner: prints H1_market_size slice from results/benchmark.json.
Full logic lives in 09_full_benchmark.py (single deterministic pipeline)."""
import json, pathlib
p = pathlib.Path(__file__).resolve().parents[1] / "results" / "benchmark.json"
print(open(p).read() if False else json.dumps(json.load(open(p))["hypotheses"].get("H1_market_size"), indent=2))
