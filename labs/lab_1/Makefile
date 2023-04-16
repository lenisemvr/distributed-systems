.DEFAULT_GOAL:=help

##@ Install Requirements
.PHONY: install-requirements
install-requirements: ## install the requirements
	@echo "Installing requirements"
	pip install -r requirements.txt

##@ Lint
.PHONY: lint
lint: ## runs pylint
	@echo "Running linter"
	pylint passive_side.py active_side.py

##@ Run Passive Side
.PHONY: run-passive-side
run-passive-side: ## runs passive-side
	python3 passive_side.py

##@ Run Active Side
.PHONY: run-active-side
run-active-side: ## runs active-side
	python3 active_side.py

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: install-requirements lint run-passive-side run-active-side