# Purpose: one-word commands to test, lint and regenerate every example output.
# Book: Coding Agents in the Enterprise, Chapters 2-12 (all tools)
# Licence: MIT (see LICENSE)
#
#   make install   install the pinned dependencies
#   make test      run the test suite
#   make lint      run the linter
#   make examples  run every tool and save its output in examples/*.md

PYTHON ?= python3
# e.g. make install PIP_FLAGS=--break-system-packages (system Python without a venv)
PIP_FLAGS ?=

.PHONY: install test lint examples data all

all: lint test examples

install:
	$(PYTHON) -m pip install $(PIP_FLAGS) PyYAML==6.0.3 pytest==9.1.1 ruff==0.17.1

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

# Regenerate the seeded synthetic datasets (output is identical on every run).
data:
	$(PYTHON) pilot/make_synthetic.py
	$(PYTHON) metrics/make_sample.py

examples:
	mkdir -p examples
	$(PYTHON) cost/cost_model.py cost/example-bank.yaml > examples/cost.md
	$(PYTHON) scorecard/score.py scorecard/example-scores.yaml > examples/scorecard.md
	$(PYTHON) pilot/sample_size.py --sd 1.2 --effect 0.4 --team-size 8 --icc 0.10 \
		> examples/sample-size.md
	$(PYTHON) pilot/did.py pilot/synthetic-pilot.csv --metric prs_per_engineer > examples/did.md
	$(PYTHON) metrics/collect.py --offline metrics/sample-prs.json \
		--since 2026-07-01 --until 2026-10-01 --out examples/metrics.json
	$(PYTHON) metrics/report.py examples/metrics.json --quarter 2026-Q3 > examples/metrics.md
	@echo "Example outputs written to examples/"
