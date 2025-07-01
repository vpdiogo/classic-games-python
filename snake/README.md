# Snake Game (Alpha)

🚧 **This is an alpha version** - Features are complete but may contain bugs. Please report any issues!

## Version: 0.1.0-alpha.1

A modern implementation of the classic Snake game built with Python and Pygame, featuring a complete menu system, configurable settings, high score tracking, and both wall collision and wrap-around gameplay modes.

### Alpha Status
- ✅ Core gameplay implemented
- ✅ Menu system working
- ✅ Configuration system
- ✅ High scores
- ⚠️  May contain bugs
- ⚠️  APIs may change
- 🧪 Feedback welcome!

## Features

### 🎮 Gameplay Features
- **Classic Snake mechanics** with smooth grid-based movement
- **Configurable wall collision**: Choose between classic walls or wrap-around teleportation
- **Dynamic food spawning** that avoids the snake's body
- **Growing snake** that increases in length with each food consumed
- **Smart collision detection** for walls and self-collision

### 🎯 Scoring System
- **Points per food**: Configurable scoring (default: 10 points per food)
- **High score tracking** with persistent storage
- **Top 10 leaderboard** with player names and timestamps
- **Personal best tracking** for individual players

### 🎛️ Menu System
- **Main Menu**: Start game, access settings, view high scores, or quit
- **Settings Menu**:
  - Toggle wall collision on/off
  - Adjust game speed (5-30 FPS)
  - Reset to default settings
- **High Scores Menu**: View top 10 scores with player names and dates
- **Pause Menu**: In-game pause with restart and menu options

### ⚙️ Configuration
- **Persistent settings** saved to `config.json`
- **Customizable window size** and grid dimensions
- **Adjustable game speed** with multiple presets
- **Flexible scoring system**
- **Validation** for all configuration values

### 🕹️ Enhanced Controls
- **Multiple input methods**: Arrow keys and WASD
- **Context-sensitive quit**: Q only works in menus and pause/game over screens
- **Smart direction buffering** prevents reverse movement
- **Responsive input handling** with one direction change per frame

## Controls

### In-Game
- **Arrow Keys** or **WASD**: Move the snake
- **Space**: Pause/Unpause the game
- **R**: Restart the current game

### In Menus
- **Arrow Keys** or **WASD**: Navigate menu options
- **Enter** or **Space**: Select menu item
- **Escape** or **Q**: Go back/quit
- **R**: Restart (in pause and game over screens)
- **Q**: Return to main menu (in pause and game over screens)

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Pygame library

### Installation
1. Clone or download the game files
2. Install dependencies:
```bash
pip install pygame
```

### Running the Game
```bash
cd snake
python run_snake.py
```

## Game Modes

### Classic Mode (Wall Collision ON)
- Snake dies when hitting walls
- Traditional Snake gameplay
- More challenging experience

### Wrap-Around Mode (Wall Collision OFF)
- Snake teleports to opposite side when hitting walls
- Modern gameplay variation
- More forgiving for beginners

## Configuration

The game automatically creates and manages configuration files:

- **`config.json`**: Game settings (automatically created on first run)
- **`high_scores.json`**: High score data (automatically created when first score is achieved)

### Default Settings
```json
{
  "WINDOW_WIDTH": 640,
  "WINDOW_HEIGHT": 480,
  "GRID_SIZE": 20,
  "FPS": 10,
  "WALL_COLLISION": true,
  "POINTS_PER_FOOD": 10,
  "INITIAL_SNAKE_LENGTH": 3
}
```

## Code Architecture

### Project Structure
```
snake/
├── src/
│   ├── config.py          # Configuration management
│   ├── game.py            # Main game logic and loop
│   ├── game_objects.py    # Snake, Food, Position classes
│   ├── input_handler.py   # Input management system
│   ├── high_score.py      # High score tracking
│   ├── logger.py          # Logging system
│   └── menu.py            # Menu system
├── tests/                 # Unit tests
├── logs/                  # Game logs
├── config.json           # Game configuration
├── high_scores.json      # High score data
└── run_snake.py          # Game launcher
```

### Key Classes

- **`SnakeGame`**: Main game controller with state management
- **`Snake`**: Snake entity with movement, growth, and collision logic
- **`Food`**: Food entity with smart spawning algorithms
- **`Position`**: Grid position with boundary and wrapping logic
- **`MenuManager`**: Complete menu system with navigation
- **`HighScoreManager`**: Persistent high score tracking
- **`InputHandler`**: Configurable input mapping system
- **`GameConfig`**: Centralized configuration with validation

## Development Features

### Testing
Run the test suite:
```bash
cd snake
pytest tests/
```

### Logging
- Comprehensive logging to `logs/snake_game.log`
- Console output for important events
- Debug information for development

### Code Quality
- **Type hints** throughout the codebase
- **Comprehensive documentation** with docstrings
- **Unit tests** for core functionality
- **Modular design** with clear separation of concerns
- **Error handling** with graceful fallbacks

## Gameplay Tips

1. **Start slow**: Begin with lower speeds to master the controls
2. **Plan ahead**: Think several moves in advance, especially as the snake grows
3. **Use walls strategically**: In wrap-around mode, use teleportation to your advantage
4. **Practice pausing**: Use the pause feature to plan difficult moves
5. **Learn the patterns**: Food spawning avoids the snake, so longer snakes have more predictable food placement

## Customization

The game is designed to be easily customizable:

- **Add new themes**: Modify colors in `config.py`
- **Change controls**: Update key mappings in `input_handler.py`
- **Adjust difficulty**: Modify speeds, scoring, or snake length in settings
- **Add features**: The modular design supports easy feature additions

## Technical Highlights

- **Grid-based movement system** for precise control
- **Efficient collision detection** using position hashing
- **Smart food placement** avoiding occupied positions
- **Persistent data storage** with JSON serialization
- **Robust error handling** with automatic recovery
- **Memory-efficient** rendering with pygame optimization
- **Cross-platform compatibility** (Windows, macOS, Linux)

---

**Enjoy playing Snake!** 🐍

For issues or suggestions, please check the code documentation or logs for troubleshooting information.