# Classic Games Python - Development Guide

## Monorepo Structure

This repository follows a monorepo approach where each game is an independent Python package with its own:
- Build system
- Tests
- Documentation
- Release process

## Quick Start

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/yourusername/classic-games-python.git
cd classic-games-python

# Global setup (optional)
make dev-setup

# Work with specific game
cd snake/
make dev-setup
```

### Daily Development Commands
```bash
# Global commands (from root)
make build        # Build all games
make test         # Test all games
make check        # Quality checks all games
make clean        # Clean all builds

# Game-specific commands (from game directory)
cd snake/
make test         # Test just snake
make build        # Build just snake
make run          # Play the game
```

## Adding New Games

### 1. Create Game Directory
```bash
mkdir newgame/
cd newgame/
```

### 2. Copy Base Structure
```bash
# Copy structure from Snake (recommended template)
cp ../snake/pyproject.toml .
cp ../snake/Makefile .
cp -r ../snake/scripts/ .
cp -r ../snake/docs/ .
mkdir -p newgame_package/ tests/
```

### 3. Update Configuration

#### pyproject.toml
```toml
[project]
name = "newgame-classic"
version = "0.1.0-alpha.1"
description = "Classic NewGame implementation"
# ... update other fields
```

#### Makefile
```makefile
# Update tag-and-push target
tag-and-push: ## Tag current version and push
	@VERSION=$$($(PYTHON) -c 'from newgame_package import __version__; print(__version__)'); \
	cd .. && \
	git tag "newgame-v$$VERSION" && \
	git push origin "newgame-v$$VERSION"
```

### 4. Update CI/CD

Add to `.github/workflows/classic-games-ci-cd.yml`:

```yaml
jobs:
  detect-changes:
    outputs:
      snake: ${{ steps.changes.outputs.snake }}
      newgame: ${{ steps.changes.outputs.newgame }}  # Add this
    steps:
    - uses: dorny/paths-filter@v2
      with:
        filters: |
          snake: ['snake/**']
          newgame: ['newgame/**']  # Add this

  test-newgame:  # Add complete job
    needs: detect-changes
    if: needs.detect-changes.outputs.newgame == 'true' || startsWith(github.ref, 'refs/tags/newgame-v')
    # ... similar to test-snake

  build-newgame:  # Add complete job
    # ... similar to build-snake

  release-newgame:  # Add complete job
    # ... similar to release-snake
```

### 5. Update Global Scripts

Add to `scripts/build-all.sh`:
```bash
build_game "NewGame" "newgame"
test_game "NewGame" "newgame"
```

## Git Workflow

### Branch Strategy
```bash
# Feature development
git checkout -b feature/game-name-feature

# Bug fixes
git checkout -b fix/game-name-bugfix

# New game development
git checkout -b game/newgame-initial-implementation
```

### Tagging Strategy
Each game has independent tags:
- `snake-v1.0.0`, `snake-v1.1.0`, etc.
- `pong-v1.0.0`, `pong-v1.1.0`, etc.
- `tetris-v1.0.0`, etc.

### Release Process
```bash
# 1. Make changes in game directory
cd snake/
# ... make changes

# 2. Test thoroughly
make test
make check

# 3. Update version and build
make build

# 4. Create release (auto-tags and pushes)
make release
make tag-and-push

# 5. GitHub Actions automatically:
#    - Runs tests on multiple Python versions
#    - Builds executables for Linux + Windows
#    - Creates GitHub release with artifacts
```

## CI/CD System

### Smart Detection
The CI/CD system detects which games changed and only:
- Tests affected games
- Builds affected games
- Creates releases for tagged games

### Workflow Structure
```yaml
detect-changes → test-game → build-game → release-game
                     ↓           ↓           ↓
                 (per game)  (per game)  (if tagged)
```

### Testing Strategy
- **Unit tests**: Each game has comprehensive test suite
- **Integration tests**: Game logic and components
- **Build tests**: Package and executable creation
- **Multi-platform**: Linux, Windows executables

## Code Quality

### Standards
- **Python 3.8+** compatibility
- **Type hints** throughout codebase
- **Docstrings** for all public functions/classes
- **Black** code formatting
- **Flake8** linting
- **MyPy** type checking

### Pre-commit Hooks
```bash
# Setup (per game)
cd snake/
pip install pre-commit
pre-commit install
```

### Quality Checks
```bash
# Manual quality checks
make check          # All games
cd snake/ && make check   # Specific game
```

## Documentation Standards

### File Structure
```
game/
├── README.md           # Game overview, quick start
├── docs/
│   ├── INSTALL.md     # Installation instructions
│   ├── DEVELOPMENT.md # Development guide
│   └── QUICK_REFERENCE.md # Command reference
└── CHANGELOG.md       # Version history
```

### README Structure
1. **Game description** and features
2. **Quick start** instructions
3. **Installation options**
4. **Controls** and gameplay
5. **Development** setup
6. **Contributing** guidelines

## Troubleshooting

### Common Issues

#### "Game not building"
```bash
cd game/
make clean
pip install -e .[dev]
make build
```

#### "Tests failing"
```bash
cd game/
pytest tests/ -v --tb=short
```

#### "CI/CD not triggering"
- Check branch name patterns in workflow
- Verify tag format: `game-v1.0.0`
- Check file paths in `paths:` filters

#### "Release not created"
- Ensure tag follows pattern: `game-v*`
- Check GitHub Actions logs
- Verify `GITHUB_TOKEN` permissions

### Debug Commands
```bash
# Repository health check
make info
make git-status

# Simulate CI locally
make ci

# Check specific game
cd snake/
make check
make test
```

## Best Practices

### Code Organization
- **Modular design** - Separate concerns clearly
- **Reusable components** - Extract common functionality
- **Clear interfaces** - Well-defined public APIs
- **Error handling** - Graceful failure modes

### Testing
- **Test coverage** - Aim for >80% coverage
- **Test types** - Unit, integration, and functional tests
- **Mocking** - Mock external dependencies
- **Fixtures** - Reusable test data and setup

### Documentation
- **Keep updated** - Documentation matches code
- **Examples** - Practical usage examples
- **Screenshots** - Visual documentation when helpful
- **Changelogs** - Track changes between versions

### Releases
- **Semantic versioning** - MAJOR.MINOR.PATCH
- **Pre-releases** - alpha, beta, rc for testing
- **Release notes** - Clear description of changes
- **Backwards compatibility** - Maintain API compatibility

---

**Happy developing!** 🎮🚀
