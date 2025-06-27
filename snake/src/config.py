"""
Centralized game configurations for Snake Game
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class GameConfig:
    """Immutable game configuration settings"""

    # Window dimensions
    WINDOW_WIDTH: int = 640
    WINDOW_HEIGHT: int = 480
    GRID_SIZE: int = 20

    # Game speed
    FPS: int = 10

    # Scoring
    POINTS_PER_FOOD: int = 10

    # Snake initial settings
    INITIAL_SNAKE_LENGTH: int = 3

    @property
    def grid_width(self) -> int:
        """Calculate grid width based on window width and grid size"""
        return self.WINDOW_WIDTH // self.GRID_SIZE

    @property
    def grid_height(self) -> int:
        """Calculate grid height based on window height and grid size"""
        return self.WINDOW_HEIGHT // self.GRID_SIZE

    @property
    def center_x(self) -> int:
        """Get center X position in grid coordinates"""
        return self.grid_width // 2

    @property
    def center_y(self) -> int:
        """Get center Y position in grid coordinates"""
        return self.grid_height // 2


@dataclass(frozen=True)
class Colors:
    """Game color palette"""

    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    DARK_GREEN: Tuple[int, int, int] = (0, 128, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    GRAY: Tuple[int, int, int] = (128, 128, 128)


# Global configuration instances
CONFIG = GameConfig()
COLORS = Colors()
