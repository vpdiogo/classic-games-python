"""
Core game objects for Snake Game
"""

import pygame
import random
from enum import Enum
from typing import List, Tuple, Optional
from .config import CONFIG, COLORS
from .logger import logger


class Direction(Enum):
    """Enum for possible movement directions"""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Position:
    """Represents a position on the game grid"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        """Check equality with another Position"""
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        """Make Position hashable for use in sets"""
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"Position({self.x}, {self.y})"

    def __add__(self, direction: Direction) -> 'Position':
        """Add a direction to get a new position"""
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

    def to_pixel(self) -> Tuple[int, int]:
        """Convert grid position to pixel coordinates"""
        return (self.x * CONFIG.GRID_SIZE, self.y * CONFIG.GRID_SIZE)

    def is_within_bounds(self) -> bool:
        """Check if position is within game boundaries"""
        return (
            0 <= self.x < CONFIG.grid_width
            and 0 <= self.y < CONFIG.grid_height
        )

    def distance_to(self, other: 'Position') -> float:
        """Calculate Manhattan distance to another position"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def wrap_around(self) -> 'Position':
        """Wrap position around game boundaries (teleport to opposite side)"""
        new_x = self.x % CONFIG.grid_width
        new_y = self.y % CONFIG.grid_height
        return Position(new_x, new_y)


class Food:
    """Represents food in the game"""

    def __init__(self):
        self.position = self._generate_random_position()
        logger.debug(f"Food spawned at {self.position}")

    def _generate_random_position(self) -> Position:
        """Generate a random position within game boundaries"""
        x = random.randint(0, CONFIG.grid_width - 1)
        y = random.randint(0, CONFIG.grid_height - 1)
        return Position(x, y)

    def respawn(self, avoid_positions: List[Position]) -> None:
        """Respawn food avoiding specified positions (usually snake body)"""
        max_attempts = 100  # Prevent infinite loop
        attempts = 0

        while attempts < max_attempts:
            new_position = self._generate_random_position()
            if new_position not in avoid_positions:
                self.position = new_position
                logger.debug(f"Food respawned at {self.position}")
                return
            attempts += 1

        # Fallback: find first available position
        for x in range(CONFIG.grid_width):
            for y in range(CONFIG.grid_height):
                candidate = Position(x, y)
                if candidate not in avoid_positions:
                    self.position = candidate
                    logger.warning(
                        f"Food respawned using fallback at {self.position}"
                    )
                    return

        logger.error("Could not find valid position for food respawn")

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the food on the screen"""
        pixel_pos = self.position.to_pixel()

        # Draw main food rectangle
        pygame.draw.rect(
            screen,
            COLORS.RED,
            (pixel_pos[0], pixel_pos[1], CONFIG.GRID_SIZE, CONFIG.GRID_SIZE),
        )

        # Draw border for better visibility
        pygame.draw.rect(
            screen,
            COLORS.WHITE,
            (pixel_pos[0], pixel_pos[1], CONFIG.GRID_SIZE, CONFIG.GRID_SIZE),
            1,
        )


class Snake:
    """Represents the snake in the game"""

    def __init__(self):
        # Initialize snake at center of screen
        self.body = self._create_initial_body()
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT  # Input buffer
        self.grow_pending = False

        logger.info(f"Snake initialized with {len(self.body)} segments")

    def _create_initial_body(self) -> List[Position]:
        """Create initial snake body"""
        center_x = CONFIG.center_x
        center_y = CONFIG.center_y

        body = []
        for i in range(CONFIG.INITIAL_SNAKE_LENGTH):
            body.append(Position(center_x - i, center_y))

        return body

    def move(self) -> None:
        """Move the snake one position forward"""
        # Apply buffered direction
        self.direction = self.next_direction

        # Calculate new head position
        new_head = self.body[0] + self.direction

        # Handle wrap-around at boundaries
        new_head = new_head.wrap_around()

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail if not growing
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
            logger.debug(f"Snake grew to {len(self.body)} segments")

    def change_direction(self, new_direction: Direction) -> bool:
        """Change snake direction (prevents reverse movement)"""
        # Define opposite directions
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        # Prevent reverse movement
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
            logger.debug(f"Direction changed to {new_direction}")
            return True

        logger.debug(
            f"Invalid direction change to {new_direction} (reverse movement)"
        )
        return False

    def grow(self) -> None:
        """Mark that snake should grow on next move"""
        self.grow_pending = True

    def check_collision(self) -> bool:
        """Check if snake has collided with walls or itself"""
        head = self.body[0]

        # Check wall collision
        # if not head.is_within_bounds():
        #     logger.info(f"Snake hit wall at {head}")
        #     return True

        # Check self collision
        if head in self.body[1:]:
            logger.info(f"Snake hit itself at {head}")
            return True

        return False

    def ate_food(self, food: Food) -> bool:
        """Check if snake ate the food"""
        if self.body[0] == food.position:
            logger.debug("Snake ate food")
            return True
        return False

    def get_length(self) -> int:
        """Get current snake length"""
        return len(self.body)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the snake on the screen"""
        for i, segment in enumerate(self.body):
            pixel_pos = segment.to_pixel()

            # Different color for head
            color = COLORS.DARK_GREEN if i == 0 else COLORS.GREEN

            # Draw segment
            pygame.draw.rect(
                screen,
                color,
                (
                    pixel_pos[0],
                    pixel_pos[1],
                    CONFIG.GRID_SIZE,
                    CONFIG.GRID_SIZE,
                ),
            )

            # Draw border
            pygame.draw.rect(
                screen,
                COLORS.BLACK,
                (
                    pixel_pos[0],
                    pixel_pos[1],
                    CONFIG.GRID_SIZE,
                    CONFIG.GRID_SIZE,
                ),
                1,
            )
