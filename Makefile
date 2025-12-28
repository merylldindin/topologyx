PYTHON_FILES = $(shell find src examples -iname "*.py" -not -path "**/__pycache__/**")

.PHONY: setup setup-hard format format-fix lint lint-fix types test test-coverage uv-lock uv-update marimo help

setup: ## Install developer experience
	@uv sync
	@uv run pre-commit install --install-hooks || echo "Warning: pre-commit hooks not installed"

setup-hard: ## Clean install from scratch
	@rm -rf .venv uv.lock
	@make setup

format: ## Check code formatting
	@uv run ruff format --check $(PYTHON_FILES)

format-fix: ## Format code with Ruff
	@uv run ruff format $(PYTHON_FILES)

lint: ## Lint code with Ruff
	@uv run ruff check $(PYTHON_FILES)

lint-fix: ## Auto-fix linting issues
	@uv run ruff check --fix $(PYTHON_FILES)

types: ## Type check with ty
	@uv run ty check

test: ## Run test suite
	@uv run pytest tests/

test-coverage: ## Run tests with coverage
	@uv run pytest tests/ --cov=src/topologyx --cov-report=term-missing

uv-lock: ## Lock dependencies
	@uv lock

uv-update: ## Update dependencies
	@uv lock --upgrade

marimo: ## Launch Marimo notebook server
	@uv run marimo edit examples/

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
