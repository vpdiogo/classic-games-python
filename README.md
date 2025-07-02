# Classic Games Python

A collection of classic game implementations built with Python and Pygame for learning and practicing game development concepts.

## About

This repository contains recreations of timeless games, designed to demonstrate fundamental game development principles and serve as educational resources for aspiring game developers.

## Games Included

### 🐍 Snake
A modern implementation of the classic Snake game featuring:
- Complete menu system with settings
- Configurable gameplay modes (wall collision vs wrap-around)
- High score tracking and leaderboards
- Persistent configuration system
- Comprehensive test suite

[**Play Snake →**](snake/)

## Learning Objectives

Through these game implementations, you'll explore:

- **Game Loop Architecture** - Understanding the core update/render cycle
- **Input Handling** - Responsive and configurable control systems
- **State Management** - Menu systems, game states, and transitions
- **Collision Detection** - Efficient algorithms for game physics
- **Data Persistence** - Saving configurations and high scores
- **Code Organization** - Modular design and clean architecture
- **Testing** - Unit tests for game logic and components
- **Configuration Management** - Flexible game settings systems

## Technologies

- **Python 3.8+** - Core programming language
- **Pygame** - Game development library for graphics, sound, and input
- **JSON** - Data storage for configurations and scores
- **Pytest** - Testing framework for quality assurance

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/classic-games-python.git
   cd classic-games-python
   ```

2. **Install dependencies**
   ```bash
   pip install pygame pytest
   ```

3. **Choose a game and start playing**
   ```bash
   cd snake
   python run_snake.py
   ```

## Project Structure

```
classic-games-python/
├── snake/              # Snake game implementation
│   ├── src/           # Game source code
│   ├── tests/         # Unit tests
│   └── README.md      # Game-specific documentation
└── README.md          # This file
```

## Contributing

This repository is primarily for educational purposes. Feel free to:
- Study the code and learn from the implementations
- Suggest improvements or optimizations
- Report bugs or issues
- Fork and create your own variations

## Game Development Concepts Covered

### Architecture Patterns
- **Entity-Component Systems** - Game object organization
- **State Machines** - Game state management
- **Observer Pattern** - Event handling and notifications

### Core Systems
- **Rendering Pipeline** - Efficient graphics updates
- **Input Processing** - Event-driven input handling
- **Audio Management** - Sound effects and music integration
- **Resource Management** - Asset loading and memory optimization

### Advanced Topics
- **Performance Optimization** - Frame rate management and efficiency
- **Configuration Systems** - Flexible game settings
- **Logging and Debugging** - Development and troubleshooting tools
- **Testing Strategies** - Automated testing for game logic

## Future Games

Planned additions to expand the learning experience:
- **Pong** - Basic physics and AI opponents
- **Tetris** - Complex piece rotation and line clearing
- **Breakout** - Ball physics and block destruction
- **Pac-Man** - Pathfinding and ghost AI
- **Space Invaders** - Projectile systems and enemy patterns

---

**Happy coding and game development learning!** 🎮

*This repository is designed for educational purposes and skill development in Python game programming with Pygame.*
