.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@ poetry run pre-commit install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml

BUMP ?= patch

.PHONY: version
version: ## Bump version (or set VERSION=x.y.z)
	@if [ "$$(git branch --show-current)" != "main" ]; then \
		echo "Must be on main"; \
		exit 1; \
	fi
	@echo "🚀 Bumping version"
	@if [ -n "$(VERSION)" ]; then \
		poetry version "$(VERSION)"; \
	else \
		poetry version "$(BUMP)"; \
	fi
	@VERSION=$$(poetry version -s); \
	echo "__version__ = '$$VERSION'" > tdemocracy/__init__.py; \
	pre-commit; \
	git add tdemocracy/__init__.py pyproject.toml; \
	git commit -m "Bump version to $$VERSION"; \
	git tag -a "v$$VERSION" -m "Bump version to $$VERSION"


.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: publish
publish: ## publish a release to pypi.
	@echo "🚀 Publishing: Dry run."
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	@poetry publish --dry-run
	@echo "🚀 Publishing."
	@poetry publish

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: docs
docs: ## Build documentation
	@echo "🚀 Building documentation"
	@poetry run sphinx-build -b html docs docs/_build/html

.DEFAULT_GOAL := help
