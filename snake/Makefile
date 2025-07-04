.PHONY: help install test lint format build clean release dev-setup check
.DEFAULT_GOAL := help

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy

help: ## Show this help message
	@echo "Snake Game Development Commands"
	@echo "==============================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick Start:"
	@echo "  make dev-setup    # First time setup"
	@echo "  make test         # Run tests"
	@echo "  make build        # Build package"

dev-setup: ## Setup development environment
	@echo "🚀 Setting up development environment..."
	@chmod +x scripts/*.sh
	@./scripts/setup-dev.sh

install: ## Install package in development mode
	@echo "📦 Installing package in development mode..."
	@$(PIP) install -e .[dev]

test: ## Run all tests with coverage
	@echo "🧪 Running test suite..."
	@chmod +x scripts/test.sh
	@./scripts/test.sh

test-quick: ## Run tests quickly without coverage
	@echo "⚡ Running quick tests..."
	@$(PYTEST) tests/ -q

test-verbose: ## Run tests with verbose output
	@echo "📋 Running verbose tests..."
	@$(PYTEST) tests/ -v --cov=snake_game --cov-report=term-missing

check: ## Run quality checks
	@echo "🔍 Running quality checks..."
	@chmod +x scripts/check.sh
	@./scripts/check.sh

lint: ## Run linting only
	@echo "🔎 Running linting..."
	@$(FLAKE8) --max-line-length=80 snake_game/ tests/
	@$(MYPY) snake_game/ --ignore-missing-imports

format: ## Format code with Black
	@echo "🎨 Formatting code..."
	@$(BLACK) --line-length 80 snake_game/ tests/ *.py

format-check: ## Check if code is formatted
	@echo "🎨 Checking code formatting..."
	@$(BLACK) --check --line-length 80 snake_game/ tests/ *.py

build: ## Build package and executable
	@echo "🏗️ Building package..."
	@chmod +x scripts/build.sh
	@./scripts/build.sh

build-wheel: ## Build only wheel package
	@echo "📦 Building wheel package..."
	@$(PYTHON) -m build --wheel

build-exe: ## Build only executable
	@echo "🔨 Building executable..."
	@$(PYTHON) -m PyInstaller snake_game.spec --clean --noconfirm

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@find . -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -path ./.venv -prune -o -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache/
	@rm -rf htmlcov/
	@rm -rf .coverage
	@rm -rf .mypy_cache/
	@echo "✅ Cleanup complete"

release: ## Create a full release
	@echo "🚀 Creating release..."
	@chmod +x scripts/release.sh
	@./scripts/release.sh

tag-and-push: ## Tag current version and push (triggers GitHub Actions)
	@echo "🏷️ Creating and pushing Snake tag..."
	@VERSION=$$($(PYTHON) -c 'from snake_game import __version__; print(__version__)' 2>&1 | tail -1); \
	cd .. && \
	git tag "snake-v$$VERSION" && \
	git push origin "snake-v$$VERSION" && \
	echo "✅ Tag snake-v$$VERSION pushed - GitHub Actions will handle the release"

# Development helpers
run: ## Run the game directly
	@echo "🎮 Starting Snake Game..."
	@$(PYTHON) run_snake.py

run-debug: ## Run game with debug logging
	@echo "🐛 Starting Snake Game (debug mode)..."
	@SNAKE_LOG_LEVEL=DEBUG $(PYTHON) run_snake.py

version: ## Show current version
	@$(PYTHON) -c "from snake_game import __version__; print(f'Version: {__version__}')" 2>&1 | tail -1

# Version bumping
bump-build: ## Bump build version (e.g., 0.1.0-alpha.1 -> 0.1.0-alpha.2)
	@echo "📈 Bumping build version..."
	@bumpversion build

bump-minor: ## Bump minor version (e.g., 0.1.0 -> 0.2.0)
	@echo "📈 Bumping minor version..."
	@bumpversion minor

bump-major: ## Bump major version (e.g., 0.1.0 -> 1.0.0)
	@echo "📈 Bumping major version..."
	@bumpversion major

bump-release: ## Change release type (alpha -> beta -> rc -> final)
	@echo "📈 Bumping release type..."
	@bumpversion release

# Install tools
install-tools: ## Install development tools
	@echo "🔧 Installing development tools..."
	@$(PIP) install build twine pyinstaller bumpversion pre-commit
	@$(PIP) install black flake8 mypy pytest-cov

# Docker support (future)
docker-build: ## Build Docker image (future feature)
	@echo "🐳 Docker support coming soon..."

# Documentation
docs: ## Generate documentation (future feature)
	@echo "📚 Documentation generation coming soon..."

# Git helpers
git-status: ## Show git status
	@git status

git-clean-check: ## Check if git working directory is clean
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "❌ Working directory is not clean"; \
		git status --short; \
		exit 1; \
	else \
		echo "✅ Working directory is clean"; \
	fi

# Continuous Integration simulation
ci: ## Run CI-like checks locally
	@echo "🤖 Running CI simulation..."
	@make clean
	@make check
	@make build
	@echo "✅ CI simulation complete"

# Performance testing
profile: ## Run performance profiling
	@echo "📊 Running performance profile..."
	@$(PYTHON) -m cProfile -o profile.stats run_snake.py || true
	@$(PYTHON) -c "import pstats; pstats.Stats('profile.stats').sort_stats('tottime').print_stats(10)" || echo "Profiling data not available"

# Information commands
info: ## Show project information
	@echo "Snake Game Project Information"
	@echo "============================="
	@echo "Version: $$($(PYTHON) -c 'from snake_game import __version__; print(__version__)')"
	@echo "Author: $$($(PYTHON) -c 'from snake_game import __author__; print(__author__)')"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pygame: $$($(PYTHON) -c 'import pygame; print(pygame.version.ver)' 2>/dev/null || echo 'Not installed')"
	@echo "Platform: $$(uname -s)"
	@echo "Directory: $$(pwd)"

# Safety checks
check-deps: ## Check if all dependencies are installed
	@echo "🔍 Checking dependencies..."
	@$(PYTHON) -c "import pygame; print('✅ pygame')" || echo "❌ pygame missing"
	@$(PYTHON) -c "import pytest; print('✅ pytest')" || echo "❌ pytest missing"
	@$(PYTHON) -c "import black; print('✅ black')" || echo "❌ black missing"
	@$(PYTHON) -c "import flake8; print('✅ flake8')" || echo "❌ flake8 missing"
