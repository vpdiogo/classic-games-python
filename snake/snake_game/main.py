"""Main entry point for the Snake Game package"""

import sys
import pygame
from .game import SnakeGame


def main():
    """Main entry point for the Snake game"""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
