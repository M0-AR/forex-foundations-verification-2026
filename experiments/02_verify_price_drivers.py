"""Thin runner: prints H8_news_nfp slice from results/benchmark.json.
Full logic lives in 09_full_benchmark.py (single deterministic pipeline)."""
import json, pathlib
p = pathlib.Path(__file__).resolve().parents[1] / "results" / "benchmark.json"
print(open(p).read() if False else json.dumps(json.load(open(p))["hypotheses"].get("H8_news_nfp"), indent=2))
