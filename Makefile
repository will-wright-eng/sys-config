#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
PYTHONPATH := `pwd`

#* Docker variables
IMAGE := sys_config
VERSION := latest

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

.DEFAULT_GOAL := help

help: ## This is help
	@echo ${MAKEFILE_LIST}
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#* Poetry
# .PHONY: poetry-download
poetry-download: ## poetry-download
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -

# .PHONY: poetry-remove
poetry-remove: ## poetry-remove
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) - --uninstall

#* Installation
# .PHONY: install
install: ## install
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	#poetry install -E dev -E test
	#	-poetry run mypy --install-types --non-interactive ./

# .PHONY: pre-commit-install
pre-commit-install: ## pre-commit-install
	poetry run pre-commit install

#* Formatters
# .PHONY: codestyle
codestyle: ## codestyle
	poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
# 	poetry run black --config pyproject.toml ./

# .PHONY: formatting
formatting: codestyle ## formatting

#* Linting
# .PHONY: test
test: ## test
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=sys_config tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

# .PHONY: check-codestyle
check-codestyle: ## check-codestyle
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
# 	poetry run black --diff --check --config pyproject.toml ./
	poetry run darglint --verbosity 2 sys_config tests

# .PHONY: mypy
mypy: ## mypy
	poetry run mypy --config-file pyproject.toml ./

# .PHONY: check-safety
check-safety: ## check-safety
	poetry check
	poetry run safety check --full-report
	poetry run bandit -ll --recursive sys_config tests

# .PHONY: lint
lint: test check-codestyle mypy check-safety ## lint

# .PHONY: update-dev-deps
update-dev-deps: ## update-dev-deps
	poetry add -D bandit@latest darglint@latest "isort[colors]@latest" mypy@latest pre-commit@latest pydocstyle@latest pylint@latest pytest@latest pyupgrade@latest safety@latest coverage@latest coverage-badge@latest pytest-html@latest pytest-cov@latest
	poetry add -D --allow-prereleases black@latest

#* Docker
# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
# .PHONY: docker-build
docker-build: ## docker-build
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
# .PHONY: docker-remove
docker-remove: ## docker-remove
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

#* Cleaning
# .PHONY: pycache-remove
pycache-remove: ## pycache-remove
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

# .PHONY: dsstore-remove
dsstore-remove: ## dsstore-remove
	find . | grep -E ".DS_Store" | xargs rm -rf

# .PHONY: mypycache-remove
mypycache-remove: ## mypycache-remove
	find . | grep -E ".mypy_cache" | xargs rm -rf

# .PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove: ## ipynbcheckpoints-remove
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

# .PHONY: pytestcache-remove
pytestcache-remove: ## pytestcache-remove
	find . | grep -E ".pytest_cache" | xargs rm -rf

# .PHONY: build-remove
build-remove: ## build-remove
	rm -rf build/

# .PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove ## cleanup
