# Development Workflow Guide

This document describes the complete development workflow for the Snake Game project.

## 🔄 Development Cycle

### 1. Initial Setup
```bash
# Clone and setup environment
git clone <repo>
cd snake
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install development dependencies
pip install -e .[dev]

# Setup pre-commit hooks
pre-commit install

# Or use automated setup
make dev-setup
```

### 2. Daily Development
```bash
# Before starting work
git pull origin main
git checkout -b feature/new-feature

# During development
python run_snake.py          # Quick testing
pytest tests/                # Run tests
pytest tests/ -v             # Verbose tests
pytest tests/ --cov=snake_game  # With coverage

# Code quality checks
black snake_game/ tests/      # Format code
flake8 snake_game/            # Linting
mypy snake_game/              # Type checking

# Alternative: use make commands
make test                     # Run tests
make format                   # Format code
make lint                     # Run linting
```

### 3. Before Committing
```bash
# Mandatory checklist
make check
# or
./scripts/check.sh

# Manual checks:
pytest tests/                 # ✅ All tests passing
black --check snake_game/     # ✅ Code formatted
flake8 snake_game/            # ✅ No linting warnings
mypy snake_game/              # ✅ Types correct

# Pre-commit will run automatically on git commit
git add .
git commit -m "feat: add new feature"
```

### 4. Version Management and Release
```bash
# Version bumping (modern way)
bump-my-version bump patch    # 0.1.0-alpha.1 → 0.1.1-alpha.1
bump-my-version bump minor    # 0.1.0-alpha.1 → 0.2.0-alpha.1
bump-my-version bump major    # 0.1.0-alpha.1 → 1.0.0-alpha.1
bump-my-version bump release  # 0.1.0-alpha.1 → 0.1.0-beta.1

# Or use make targets
make bump-patch               # Patch version
make bump-minor               # Minor version
make bump-major               # Major version
make bump-release             # Release type

# Create release
make release                  # Complete build + checks
# or
./scripts/release.sh
```

## 🛠️ Automation Scripts

### Available Scripts
- **`scripts/setup-dev.sh`** - Complete development environment setup
- **`scripts/test.sh`** - Comprehensive test suite with coverage
- **`scripts/check.sh`** - Code quality checks (format, lint, types)
- **`scripts/build.sh`** - Build package and executable
- **`scripts/release.sh`** - Complete release process

### Makefile Commands
```bash
# Development
make dev-setup    # Setup development environment
make install      # Install package in development mode
make clean        # Clean build artifacts

# Testing and Quality
make test         # Run all tests with coverage
make test-quick   # Run tests without coverage
make test-verbose # Run tests with verbose output
make check        # Run all quality checks
make lint         # Run linting only
make format       # Format code with Black
make format-check # Check if code is formatted

# Building and Release
make build        # Build package and executable
make build-wheel  # Build only wheel package
make build-exe    # Build only executable
make release      # Complete release process

# Version Management
make bump-patch   # Patch version (0.1.0 -> 0.1.1)
make bump-minor   # Minor version (0.1.0 -> 0.2.0)
make bump-major   # Major version (0.1.0 -> 1.0.0)
make bump-release # Release type (alpha -> beta -> rc -> final)

# Utilities
make info         # Show project information
make version      # Show current version
make help         # Show all available commands
```

## 📋 Checklists

### Before Each Commit
- [ ] Tests passing (`make test` or `pytest`)
- [ ] Code formatted (`make format` or `black`)
- [ ] Linting clean (`make lint` or `flake8`)
- [ ] Types correct (`mypy snake_game/`)
- [ ] Functionality tested manually (`python run_snake.py`)
- [ ] Pre-commit hooks passing

### Before Each Release
- [ ] All tests passing with good coverage (>50%)
- [ ] Version incremented (`bump-my-version` or `make bump-*`)
- [ ] [`CHANGELOG.md`](../CHANGELOG.md) updated with changes
- [ ] Build working (`make build` or `./scripts/build.sh`)
- [ ] Executables tested (if applicable)
- [ ] Documentation updated ([`README.md`](../README.md), [`docs/INSTALL.md`](INSTALL.md))
- [ ] Git working directory clean
- [ ] All changes committed and pushed

## 🏗️ Build System

### Modern Python Packaging (pyproject.toml)
The project uses modern Python packaging with `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "snake-game-classic"
version = "0.1.0-alpha.1"
# ... rest of configuration
```

### Local Build Commands
```bash
# Quick build for testing
python -m build

# Complete build with executables
make build
# or
./scripts/build.sh

# Only wheel package
make build-wheel

# Only executable (PyInstaller)
make build-exe
# or
pyinstaller snake_game.spec --clean --noconfirm
```

### Build Verification
```bash
# Test wheel package
pip install dist/*.whl
snake-game

# Test source installation
pip install -e .
python run_snake.py

# Test executable (if built)
./dist/SnakeGame
```

## 📦 Distribution

### PyPI (Future)
```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

### GitHub Releases
```bash
# Create tag and push
git tag v0.1.0-alpha.1
git push origin v0.1.0-alpha.1

# GitHub Actions will handle the rest
```

## 🚀 Quick Commands (Makefile)

```bash
make install    # Development setup
make test       # Run tests
make lint       # Check code
make format     # Format code
make build      # Complete build
make clean      # Clean files
make release    # Complete release
```

## 📊 Quality Metrics

### Test Coverage
- **Target**: >90% coverage
- **Command**: `pytest --cov=snake_game --cov-report=html`

### Code Quality
- **Black**: Automatic formatting
- **Flake8**: Linting and style guide
- **MyPy**: Type checking
- **Pre-commit**: Automatic hooks

## 🐛 Debugging

### Logs
```bash
# Logs em tempo real
tail -f logs/snake_game.log

# Logs com mais detalhes
export SNAKE_LOG_LEVEL=DEBUG
python run_snake.py
```

### Profiling
```bash
# Performance profiling
python -m cProfile -o profile.stats run_snake.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('tottime').print_stats(10)"
```

## 📚 Recursos Úteis

- [Python Packaging Guide](https://packaging.python.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
