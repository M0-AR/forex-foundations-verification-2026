.PHONY: verify fetch benchmark test docker-up docker-down clean

verify:
	bash scripts/run_all.sh

fetch:
	python3 experiments/00_fetch_live_data.py

benchmark:
	python3 experiments/09_full_benchmark.py

test:
	python3 -m pytest tests/ -v

docker-up:
	docker compose up --build research

docker-down:
	docker compose down -v

clean:
	rm -rf results/* data/*.csv data/*.json __pycache__ src/__pycache__ experiments/__pycache__
	mkdir -p results data
