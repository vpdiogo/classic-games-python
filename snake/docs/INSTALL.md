# Snake Game - Installation and Usage Guide (Alpha)

🚧 **Alpha Version 0.1.0-alpha.1** - Please report any bugs or issues!

## Prerequisites

- **Python 3.8+** (Required)
- **pip** (Python package manager)
- **pygame** library (will be installed automatically)

## Quick Installation & Usage

### Method 1: Install from Package (Recommended)
```bash
# Navigate to the project directory
cd snake/

# Install the package
pip install dist/snake_game_classic-0.1.0a1-py3-none-any.whl

# Run the game
snake-game
```

### Method 2: Development Mode (For Developers)
```bash
# Navigate to the project directory
cd snake/

# Install in development mode with all dependencies
pip install -e .[dev]

# Run the game
snake-game
# or
python run_snake.py
# or
python -m snake_game.main
```

### Method 3: Direct Execution (Quick Test)
```bash
# Navigate to the project directory
cd snake/

# Install only runtime dependencies
pip install pygame

# Run directly without installation
python run_snake.py
```

## Development Setup

### Complete Development Environment
```bash
# Navigate to the project directory
cd snake/

# Setup development environment (recommended)
make dev-setup

# Or manually:
pip install -e .[dev]
pre-commit install
```

### Development Dependencies Include:
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks
- **build** - Modern Python packaging
- **bump-my-version** - Version management

## Building and Packaging

### Build Python Package
```bash
# Install build tools (if not already installed)
pip install build

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build wheel and source distribution
python -m build

# Built files will be in dist/:
# - snake_game_classic-0.1.0a1-py3-none-any.whl (wheel)
# - snake_game_classic-0.1.0a1.tar.gz (source)
```

### Build Executable (PyInstaller)
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable using provided script
./scripts/build.sh

# Or manually:
pyinstaller snake_game.spec --clean --noconfirm
```

### Development Commands
```bash
# Run all tests
make test
# or
pytest tests/ -v

# Code quality checks
make check
# or
./scripts/check.sh

# Format code
black snake_game/ tests/

# Build package
make build
# or
./scripts/build.sh
```

## Version Management

### Bump Version (Modern Way)
```bash
# Patch version: 0.1.0-alpha.1 -> 0.1.1-alpha.1
bump-my-version bump patch

# Minor version: 0.1.0-alpha.1 -> 0.2.0-alpha.1
bump-my-version bump minor

# Major version: 0.1.0-alpha.1 -> 1.0.0-alpha.1
bump-my-version bump major

# Release type: 0.1.0-alpha.1 -> 0.1.0-beta.1
bump-my-version bump release
```

### Create Release
```bash
# Automated release process
./scripts/release.sh
# or
make release
```

## Game Usage

### Game Controls
- **Arrow Keys** or **WASD**: Move snake
- **Space**: Pause/Unpause
- **Enter**: Select in menus
- **Escape** or **Q**: Go back/quit
- **R**: Restart (in pause/game over screens)

### Configuration
- Game creates a `config.json` file for persistent settings
- Configure game speed, wall collision, window size, etc.
- Access settings through the in-game menu system

## Project Structure

```
snake/
├── README.md                 # Project overview
├── pyproject.toml           # Modern configuration (PEP 518/621)
├── config.json              # Game configuration
├── run_snake.py             # Game launcher
├── snake_game/              # Main package
│   ├── __init__.py          # Package metadata
│   ├── main.py              # Entry point
│   ├── game.py              # Core game logic
│   ├── menu.py              # Menu system
│   ├── game_objects.py      # Snake, Food, Position
│   ├── config.py            # Configuration management
│   ├── high_score.py        # Score tracking
│   └── assets/              # Game assets
├── tests/                   # Test suite
├── docs/                    # Documentation
│   ├── INSTALL.md           # This file
│   ├── DEVELOPMENT.md       # Development guide
│   └── QUICK_REFERENCE.md   # Command reference
└── scripts/                 # Build and development scripts
```

## Features

- ✅ **Classic Snake gameplay** with modern enhancements
- ✅ **Configurable wall collision** (classic walls or wrap-around)
- ✅ **High score tracking** with persistent storage
- ✅ **Complete menu system** with settings and high scores
- ✅ **Persistent settings** saved automatically
- ✅ **Full test coverage** (52%+ coverage)
- ✅ **Modern packaging** with pyproject.toml
- ✅ **Development tools** with pre-commit hooks
- ✅ **Quality assurance** with automated testing

## Troubleshooting

### Common Issues

**ImportError: No module named 'pygame'**
```bash
pip install pygame
```

**Permission denied when running scripts**
```bash
chmod +x scripts/*.sh
```

**Tests failing**
```bash
# Make sure you're in the snake/ directory
cd snake/
pytest tests/ -v
```

**Build failing**
```bash
# Clean and rebuild
rm -rf build/ dist/ *.egg-info/
python -m build
```

### Getting Help

- **Documentation**: See [`docs/DEVELOPMENT.md`](DEVELOPMENT.md) for detailed development guide
- **Commands**: See [`docs/QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for command reference
- **Issues**: Report bugs in the project repository

Enjoy playing! 🐍🎮
