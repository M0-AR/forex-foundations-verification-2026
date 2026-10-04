#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data results
export PYTHONPATH="$PWD:${PYTHONPATH:-}"
echo "== [1/10] fetch live data =="
python3 src/data_fetch.py || python3 -c "import src.data_fetch as m; m.main()"
echo "== [2/10] full benchmark =="
PYTHONPATH="$PWD" python3 experiments/09_full_benchmark.py
echo "== [3/10] unit tests =="
python3 -m pytest tests/ -q || true
echo "== DONE. See results/ and data/fetch_summary.json =="
ls -lh results/ data/ | head -n 60
