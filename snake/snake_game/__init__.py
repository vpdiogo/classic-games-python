"""
Snake Game - A modern implementation of the classic Snake game.

This package provides a complete Snake game with configurable settings,
high score tracking, and both wall collision and wrap-around modes.
"""

__version__ = "0.1.0-alpha.1"
__author__ = "Vitor"
__email__ = "your.email@example.com"

from .game import SnakeGame
from .config import CONFIG, COLORS

__all__ = ["SnakeGame", "CONFIG", "COLORS"]
