"""
Centralized game configurations for Snake Game
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any
import json
import os


@dataclass
class GameConfig:
    """Game configuration settings with validation"""

    # Window dimensions
    WINDOW_WIDTH: int = 640
    WINDOW_HEIGHT: int = 480
    GRID_SIZE: int = 20

    # Game settings
    FPS: int = 10
    WALL_COLLISION: bool = False

    # Scoring
    POINTS_PER_FOOD: int = 10

    # Snake initial settings
    INITIAL_SNAKE_LENGTH: int = 3

    # Configuration file path
    _config_file: str = field(default="config.json", init=False)

    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration values"""
        if self.WINDOW_WIDTH <= 0 or self.WINDOW_HEIGHT <= 0:
            raise ValueError("Window dimensions must be positive")

        if self.GRID_SIZE <= 0:
            raise ValueError("Grid size must be positive")

        if self.FPS <= 0:
            raise ValueError("FPS must be positive")

        if self.POINTS_PER_FOOD < 0:
            raise ValueError("Points per food cannot be negative")

        if self.INITIAL_SNAKE_LENGTH < 1:
            raise ValueError("Initial snake length must be at least 1")

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

    def update_setting(self, setting_name: str, value: Any) -> None:
        """Safely update a configuration setting with validation"""
        if not hasattr(self, setting_name):
            raise ValueError(f"Unknown setting: {setting_name}")

        # Store old value for rollback if validation fails
        old_value = getattr(self, setting_name)

        try:
            setattr(self, setting_name, value)
            self._validate_config()
        except ValueError as e:
            # Rollback to old value if validation fails
            setattr(self, setting_name, old_value)
            raise ValueError(f"Invalid value for {setting_name}: {e}")

    def toggle_wall_collision(self) -> None:
        """Toggle wall collision setting"""
        self.WALL_COLLISION = not self.WALL_COLLISION

    def set_fps(self, fps: int) -> None:
        """Set FPS with validation"""
        self.update_setting("FPS", fps)

    def save_to_file(self, filename: Optional[str] = None) -> None:
        """Save configuration to JSON file"""
        if filename is None:
            filename = self._config_file

        config_dict = {
            "WINDOW_WIDTH": self.WINDOW_WIDTH,
            "WINDOW_HEIGHT": self.WINDOW_HEIGHT,
            "GRID_SIZE": self.GRID_SIZE,
            "FPS": self.FPS,
            "WALL_COLLISION": self.WALL_COLLISION,
            "POINTS_PER_FOOD": self.POINTS_PER_FOOD,
            "INITIAL_SNAKE_LENGTH": self.INITIAL_SNAKE_LENGTH,
        }

        try:
            with open(filename, "w") as f:
                json.dump(config_dict, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config to {filename}: {e}")

    def load_from_file(self, filename: Optional[str] = None) -> None:
        """Load configuration from JSON file"""
        if filename is None:
            filename = self._config_file

        if not os.path.exists(filename):
            # Create default config file if it doesn't exist
            print(
                f"Config file {filename} not found. Creating default configuration."
            )
            self.save_to_file(filename)
            return

        try:
            with open(filename, "r") as f:
                config_dict = json.load(f)

            # Update settings one by one with validation
            for key, value in config_dict.items():
                if hasattr(self, key):
                    try:
                        self.update_setting(key, value)
                    except ValueError as e:
                        print(
                            f"Warning: Invalid value for {key}: {e}. Using default."
                        )

        except (IOError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config from {filename}: {e}")
            print("Creating new default configuration file.")
            self.save_to_file(filename)

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        defaults = GameConfig()
        for field_name in [
            "WINDOW_WIDTH",
            "WINDOW_HEIGHT",
            "GRID_SIZE",
            "FPS",
            "WALL_COLLISION",
            "POINTS_PER_FOOD",
            "INITIAL_SNAKE_LENGTH",
        ]:
            setattr(self, field_name, getattr(defaults, field_name))

    def get_speed_options(self) -> List[int]:
        """Get available speed options"""
        return [5, 8, 10, 15, 20, 25, 30]

    def cycle_fps(self) -> int:
        """Cycle to next FPS option and return new value"""
        speeds = self.get_speed_options()
        try:
            current_index = speeds.index(self.FPS)
            next_index = (current_index + 1) % len(speeds)
        except ValueError:
            next_index = 2  # Default to index 2 (10 FPS)

        self.FPS = speeds[next_index]
        return self.FPS


@dataclass(frozen=True)
class Colors:
    """Game color palette - kept frozen since colors shouldn't change"""

    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    DARK_GREEN: Tuple[int, int, int] = (0, 128, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    LIGHT_BLUE: Tuple[int, int, int] = (173, 216, 230)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)


# Global configuration instances
CONFIG = GameConfig()
COLORS = Colors()

# Load saved configuration on import
CONFIG.load_from_file()
