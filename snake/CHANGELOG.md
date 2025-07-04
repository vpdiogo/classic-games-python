## [0.1.0-alpha.1] - 2025-07-04

### Changes in this release:
- Bug fixes and improvements
- Updated documentation
- Package optimizations

## [0.1.0-alpha.1] - 2025-07-02

### Changes in this release:
- Bug fixes and improvements
- Updated documentation
- Package optimizations

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial alpha release preparation

## [0.1.0-alpha.1] - 2025-07-02

### Added
- ✨ Complete Snake game implementation with modern features
- 🎮 Menu system with navigation (Main Menu, Settings, High Scores)
- ⚙️ Configurable settings (wall collision toggle, game speed)
- 🏆 High score tracking with persistent storage
- 🐍 Two gameplay modes: Classic (wall collision) and Wrap-around
- 🎯 Smart food spawning that avoids snake body
- ⌨️ Multiple input methods (Arrow keys, WASD)
- ⏸️ Pause/resume functionality
- 🔄 Game restart capability
- 📊 Real-time score display
- 💾 Persistent configuration system
- 🧪 Comprehensive test suite (46 tests)
- 📦 Professional Python package structure
- 🚀 Build and release automation scripts
- 📖 Complete documentation

### Game Features
- Classic Snake mechanics with grid-based movement
- Configurable wall collision (walls vs wrap-around teleportation)
- Growing snake that increases length with each food
- Smart collision detection for walls and self-collision
- Multiple difficulty levels via speed settings

### Technical Features
- Modular architecture with clean separation of concerns
- Type hints throughout the codebase
- Comprehensive logging system
- Error handling with graceful fallbacks
- Cross-platform compatibility (Windows, macOS, Linux)
- Memory-efficient rendering
- JSON-based configuration and data storage

### Controls
- **Arrow Keys** or **WASD**: Move snake
- **Space**: Pause/Unpause game
- **R**: Restart game (in pause/game over)
- **Q**: Return to menu (in pause/game over only)
- **Enter**: Select menu items
- **Escape**: Navigate back in menus

### Package Structure
- `snake_game/` - Main game package
- `tests/` - Unit tests with 52%+ core functionality coverage
- `dist/` - Built packages for distribution
- Build automation with setuptools and bump-my-version
- GitHub Actions CI/CD pipeline ready

### Known Issues (Alpha)
- Some edge cases in wrap-around mode may need polish
- Menu transitions could be smoother
- Executable building not yet tested on all platforms

### Development
- Python 3.8+ support
- Pygame as primary dependency
- pytest for testing framework
- Full development toolchain setup
