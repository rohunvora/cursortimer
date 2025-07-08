.PHONY: help install install-dev test test-all lint format type-check security-check build clean docs serve-docs pre-commit

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run unit tests
	pytest tests/ -v

test-all:  ## Run tests across all Python versions using tox
	tox

lint:  ## Run linters
	black --check cursor_eta tests
	isort --check-only cursor_eta tests
	flake8 cursor_eta tests
	mypy cursor_eta --ignore-missing-imports --strict

format:  ## Format code
	black cursor_eta tests
	isort cursor_eta tests

type-check:  ## Run type checking
	mypy cursor_eta --ignore-missing-imports --strict

security-check:  ## Run security checks
	bandit -r cursor_eta -ll
	safety check

build:  ## Build distribution packages
	python -m build
	twine check dist/*

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:  ## Build documentation
	cd docs && make html

serve-docs:  ## Serve documentation locally
	cd docs && python -m http.server --directory _build/html

pre-commit:  ## Run pre-commit hooks
	pre-commit run --all-files

# Development shortcuts
.PHONY: dev
dev: install-dev  ## Set up development environment

.PHONY: ci
ci: lint type-check test  ## Run CI checks locally

.PHONY: release-test
release-test:  ## Test release process (dry run)
	python -m build
	twine check dist/*
	twine upload --repository testpypi dist/* --verbose