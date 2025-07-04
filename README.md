# Classic Games Python Collection 🎮

A collection of classic games implemented in Python with modern features and packaging.

## Games Collection

### 🐍 Snake Game
**Status**: ✅ Alpha Release Available
**Location**: [`snake/`](snake/)
**Version**: 0.1.0-alpha.1

Classic Snake game with modern enhancements:
- Configurable wall collision (classic walls or wrap-around)
- High score tracking with persistent storage
- Complete menu system with settings
- Cross-platform executables (Linux, Windows)
- Multiple input methods (Arrow keys, WASD)

**Quick Start**:
```bash
cd snake/
pip install -e .[dev]
python run_snake.py
```

### 🏓 Pong (Coming Soon)
**Status**: 🚧 Planned
**Location**: [`pong/`](pong/) (future)

### 🧱 Tetris (Coming Soon)
**Status**: 🚧 Planned
**Location**: [`tetris/`](tetris/) (future)
## Repository Structure

```
classic-games-python/
├── .github/workflows/          # CI/CD workflows for all games
│   └── classic-games-ci-cd.yml # Smart build system
├── snake/                      # Snake game package
│   ├── snake_game/            # Source code
│   ├── tests/                 # Tests
│   ├── docs/                  # Documentation
│   ├── scripts/               # Build scripts
│   └── pyproject.toml         # Package configuration
├── docs/                      # Global documentation
└── scripts/                   # Global build tools
```

## Development

### Prerequisites
- Python 3.8+
- pip
- git

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/yourusername/classic-games-python.git
cd classic-games-python

# Setup specific game
cd snake/
make dev-setup

# Run tests
make test

# Build package
make build
```

### CI/CD System

This monorepo uses intelligent CI/CD that:
- **Detects changes** per game automatically
- **Runs tests** only for modified games
- **Builds releases** independently for each game
## Releases

Each game has independent releases:

### Snake Game
- **Latest Release**: [Download from GitHub Releases](https://github.com/yourusername/classic-games-python/releases)
- **Executables**: SnakeGame-linux, SnakeGame-windows.exe
- **Python Package**: `snake-game-classic`

### Release Process
```bash
# For Snake
cd snake/
make release
make tag-and-push

# This triggers automatic GitHub Actions that:
# 1. Run tests on multiple Python versions
# 2. Build executables for Linux + Windows
# 3. Create GitHub release with all artifacts
```

## Installation Options

### Option 1: Download Executables
1. Go to [GitHub Releases](https://github.com/yourusername/classic-games-python/releases)
2. Download for your platform
3. Run directly - no installation needed!

### Option 2: Install Python Package
```bash
# Download wheel from GitHub Releases
pip install snake_game_classic-X.X.X-py3-none-any.whl
snake-game
```

### Option 3: Development Installation
```bash
cd snake/
pip install -e .[dev]
python run_snake.py
```

## Technology Stack

- **Language**: Python 3.8+
- **Game Engine**: Pygame
- **Testing**: pytest
- **Packaging**: Modern Python packaging (pyproject.toml)
- **CI/CD**: GitHub Actions
- **Build Tools**: PyInstaller for executables

## Game Development Concepts Covered

### Architecture Patterns
- **Entity-Component Systems** - Game object organization
- **State Machines** - Game state management
- **Observer Pattern** - Event handling and notifications

### Core Systems
- **Rendering Pipeline** - Efficient graphics updates
## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/your-feature`
3. **Make changes** in the appropriate game directory
4. **Add tests** and ensure they pass
5. **Submit pull request**

### Code Quality
- **Automated testing** with pytest
- **Code formatting** with Black
- **Linting** with Flake8 and MyPy
- **Pre-commit hooks** for quality assurance

## Documentation

- **Snake Game**: [`snake/README.md`](snake/README.md)
- **Installation Guide**: [`snake/docs/INSTALL.md`](snake/docs/INSTALL.md)
- **Development Guide**: [`snake/docs/DEVELOPMENT.md`](snake/docs/DEVELOPMENT.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/classic-games-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/classic-games-python/discussions)
- **Documentation**: See individual game directories

---

**Enjoy the games!** 🎮🚀

*Classic games with modern Python packaging and development practices.*
- **Breakout** - Ball physics and block destruction
- **Pac-Man** - Pathfinding and ghost AI
- **Space Invaders** - Projectile systems and enemy patterns

---

**Happy coding and game development learning!** 🎮

*This repository is designed for educational purposes and skill development in Python game programming with Pygame.*
