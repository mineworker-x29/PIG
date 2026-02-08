PYTHON ?= python3
VENV ?= .venv

.PHONY: setup run clean

setup:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -e . --no-build-isolation

run:
	. $(VENV)/bin/activate && pig

clean:
	rm -rf $(VENV) data/processed/ocel_stub.json
