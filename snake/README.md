# Snake Game

A classic snake game implemented in Python using Pygame.

## How to Play

### Controls
- **Arrow keys** or **WASD**: Move the snake
- **Space**: Pause/Unpause the game
- **R**: Restart the game
- **Q**: Quit the game (only on the game over screen)

### Objective
- Control the snake to eat the red food
- Each food consumed increases the score by 10 points
- The snake grows with each food eaten
- Avoid colliding with the walls or the snake's own body

## Installation and Running

1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
cd snake
python snake_game.py
```

## Code Structure

The code follows Pygame best practices and is organized into classes:

- **Position**: Class to represent positions on the grid
- **Direction**: Enum for directions (UP, DOWN, LEFT, RIGHT)
- **Food**: Class to manage the food
- **Snake**: Class to manage the snake and its logic
- **Game**: Main class that coordinates the entire game

## Features

- Grid system for precise movement
- Collision detection with walls and the snake's body
- Scoring system
- Pause and restart functionality
- Clean and intuitive visual interface
- Modular and well-documented code
