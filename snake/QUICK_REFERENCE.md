# Quick Reference Guide

## Daily Commands

```bash
# Setup (first time only)
make dev-setup

# Development workflow
make test           # Run all tests
make check          # Quality checks
make format         # Format code
make run           # Test game

# Build and release
make build         # Build package + executable
make release       # Full release process
```

## Scripts Available

- `scripts/setup-dev.sh` - Initial development setup
- `scripts/check.sh` - Quality checks (tests, linting, typing)
- `scripts/test.sh` - Comprehensive test suite
- `scripts/build.sh` - Build packages and executables
- `scripts/release.sh` - Complete release process

## Version Management

```bash
# Increment alpha build number
make bump-build     # 0.1.0-alpha.1 → 0.1.0-alpha.2

# Change release type
make bump-release   # alpha → beta → rc → final

# Increment version numbers
make bump-minor     # 0.1.0 → 0.2.0
make bump-major     # 0.1.0 → 1.0.0
```

## Testing

```bash
make test           # Full test suite with coverage
make test-quick     # Quick tests only
make test-verbose   # Detailed test output
pytest tests/       # Direct pytest
```

## Code Quality

```bash
make check          # All quality checks
make lint           # Linting only
make format         # Format code
make format-check   # Check formatting
```

## Build Outputs

After `make build` or `make release`:

- `dist/*.whl` - Python package (installable)
- `dist/*.tar.gz` - Source distribution
- `dist/SnakeGame` - Standalone executable
- `release/` - Complete release package

## Common Issues

### Import Errors
```bash
make install        # Reinstall in dev mode
```

### Test Failures
```bash
make check          # Run quality checks
make clean          # Clean build artifacts
```

### Build Problems
```bash
make clean          # Clean everything
make install        # Reinstall dependencies
make build          # Try build again
```

## File Structure

```
snake/
├── scripts/        # Development automation
├── snake_game/     # Main package
├── tests/          # Unit tests
├── dist/           # Built packages
├── release/        # Release artifacts
├── Makefile        # Quick commands
└── DEVELOPMENT.md  # Detailed guide
```
