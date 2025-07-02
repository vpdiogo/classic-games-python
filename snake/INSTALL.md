# Snake Game - Installation and Usage Guide (Alpha)

🚧 **Alpha Version 0.1.0-alpha.1** - Please report any bugs or issues!

## Quick Installation & Usage

### Method 1: Install from Package (Recommended)
```bash
# Install the package
pip install dist/snake_game_classic-1.0.0-py3-none-any.whl

# Run the game
snake-game
```

### Method 2: Development Mode
```bash
# Install in development mode (for developers)
pip install -e .

# Run the game
snake-game
# or
python run_snake.py
```

### Method 3: Direct Execution
```bash
# Run directly without installation
python -m snake_game.main
```

## Building for Distribution

### Build Python Package
```bash
# Install build tools
pip install build

# Build the package
python -m build
```

### Build Executable (coming soon)
```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
./build.sh
```

### Create Release
```bash
# Automated release process
python release.py
```

## Development

### Install Development Dependencies
```bash
pip install build pytest bumpversion pyinstaller
```

### Run Tests
```bash
pytest tests/
```

### Version Management
```bash
# Bump version automatically
bumpversion patch  # 1.0.0 -> 1.0.1
bumpversion minor  # 1.0.1 -> 1.1.0
bumpversion major  # 1.1.0 -> 2.0.0
```

## Game Controls

- **Arrow Keys** or **WASD**: Move snake
- **Space**: Pause/Unpause
- **R**: Restart (in pause/game over)
- **Q**: Quit to menu (in pause/game over)
- **Enter**: Select in menus

## Features

- ✅ Classic Snake gameplay
- ✅ Configurable wall collision (wrap-around mode)
- ✅ High score tracking
- ✅ Complete menu system
- ✅ Persistent settings
- ✅ Full test coverage

Enjoy playing! 🐍
