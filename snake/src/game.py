"""
Main game class for Snake Game
"""

import pygame
import sys
from enum import Enum
from typing import Optional
from .config import CONFIG, COLORS
from .game_objects import Snake, Food
from .input_handler import InputHandler, InputAction
from .high_score import HighScoreManager
from .logger import logger


class GameState(Enum):
    """Game state enumeration"""

    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    MENU = "menu"


class SnakeGame:
    """Main Snake Game class"""

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Setup display
        self.screen = pygame.display.set_mode(
            (CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Snake Game")

        # Game components
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game systems
        self.input_handler = InputHandler()
        self.high_score_manager = HighScoreManager()

        # Game state
        self.state = GameState.PLAYING
        self.score = 0
        self.direction_changed_this_frame = False

        # Initialize game objects
        self.reset_game()

        logger.info("Snake Game initialized")

    def reset_game(self) -> None:
        """Reset game to initial state"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.state = GameState.PLAYING
        self.direction_changed_this_frame = False

        # Ensure food doesn't spawn on snake
        self.food.respawn(self.snake.body)

        logger.info("Game reset")

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False to quit game."""
        # Reset direction change flag
        self.direction_changed_this_frame = False

        # Get all events
        events = list(pygame.event.get())

        # Check for quit events
        for event in events:
            if event.type == pygame.QUIT:
                return False

        # Get actions from input handler
        actions = self.input_handler.get_actions_from_events(events)

        # Process actions based on game state
        if self.state == GameState.GAME_OVER:
            return self._handle_game_over_actions(actions)
        else:
            return self._handle_playing_actions(actions)

    def _handle_game_over_actions(self, actions: set) -> bool:
        """Handle actions during game over state"""
        if InputAction.RESTART in actions:
            self.reset_game()
        elif InputAction.QUIT in actions:
            return False
        return True

    def _handle_playing_actions(self, actions: set) -> bool:
        """Handle actions during playing state"""
        # Handle movement actions (only one per frame)
        if not self.direction_changed_this_frame:
            for action in actions:
                if self.input_handler.is_movement_action(action):
                    direction = self.input_handler.get_direction_from_action(
                        action
                    )
                    if direction and self.snake.change_direction(direction):
                        self.direction_changed_this_frame = True
                        break

        # Handle other actions
        if InputAction.PAUSE in actions:
            was_paused = self.state == GameState.PAUSED
            self.state = GameState.PLAYING if was_paused else GameState.PAUSED

            # Clear direction buffer when unpausing
            if was_paused:
                self.snake.next_direction = self.snake.direction

            logger.info(f"Game {'unpaused' if was_paused else 'paused'}")

        elif InputAction.RESTART in actions:
            self.reset_game()

        elif InputAction.QUIT in actions:
            return False

        return True

    def update(self) -> None:
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return

        # Move snake
        self.snake.move()

        # Check collisions
        if self.snake.check_collision():
            self._handle_game_over()
            return

        # Check if snake ate food
        if self.snake.ate_food(self.food):
            self.snake.grow()
            self.score += CONFIG.POINTS_PER_FOOD
            self.food.respawn(self.snake.body)

            logger.info(
                f"Score: {self.score}, Snake length: {self.snake.get_length()}"
            )

    def _handle_game_over(self) -> None:
        """Handle game over logic"""
        self.state = GameState.GAME_OVER

        # Check and save high score
        is_high_score = self.high_score_manager.add_score(self.score)

        if is_high_score:
            logger.info(f"New high score: {self.score}")
        else:
            logger.info(f"Game over. Score: {self.score}")

    def draw_text(
        self, text: str, x: int, y: int, color=COLORS.WHITE, font=None
    ) -> None:
        """Draw text on screen"""
        if font is None:
            font = self.font

        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_centered_text(
        self, text: str, y: int, color=COLORS.WHITE, font=None
    ) -> None:
        """Draw centered text"""
        if font is None:
            font = self.font

        text_surface = font.render(text, True, color)
        x = (CONFIG.WINDOW_WIDTH - text_surface.get_width()) // 2
        self.screen.blit(text_surface, (x, y))

    def draw_hud(self) -> None:
        """Draw heads-up display"""
        # Current score
        self.draw_text(f"Score: {self.score}", 10, 10)

        # High score
        high_score = self.high_score_manager.get_high_score()
        self.draw_text(f"High Score: {high_score}", 10, 40)

        # Snake length
        self.draw_text(
            f"Length: {self.snake.get_length()}", 10, 70, font=self.small_font
        )

    def draw_game_over_screen(self) -> None:
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game over text
        self.draw_centered_text(
            "GAME OVER", CONFIG.WINDOW_HEIGHT // 2 - 60, COLORS.RED
        )

        # Final score
        self.draw_centered_text(
            f"Final Score: {self.score}", CONFIG.WINDOW_HEIGHT // 2 - 20
        )

        # High score check
        if self.score == self.high_score_manager.get_high_score():
            self.draw_centered_text(
                "NEW HIGH SCORE!", CONFIG.WINDOW_HEIGHT // 2 + 10, COLORS.BLUE
            )

        # Instructions
        self.draw_centered_text(
            "Press R to restart or Q to quit",
            CONFIG.WINDOW_HEIGHT // 2 + 50,
            font=self.small_font,
        )

    def draw_pause_screen(self) -> None:
        """Draw pause screen"""
        self.draw_centered_text(
            "PAUSED", CONFIG.WINDOW_HEIGHT // 2 - 20, COLORS.BLUE
        )
        self.draw_centered_text(
            "Press SPACE to continue",
            CONFIG.WINDOW_HEIGHT // 2 + 20,
            font=self.small_font,
        )

    def draw(self) -> None:
        """Draw all game elements"""
        # Clear screen
        self.screen.fill(COLORS.BLACK)

        # Draw game objects (if not game over)
        if self.state != GameState.GAME_OVER:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

        # Draw HUD
        self.draw_hud()

        # Draw state-specific overlays
        if self.state == GameState.PAUSED:
            self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen()

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop"""
        logger.info("Starting game loop")
        running = True

        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(CONFIG.FPS)

        except KeyboardInterrupt:
            logger.info("Game interrupted by user")

        except Exception as e:
            logger.error(f"Unexpected error in game loop: {e}")
            raise

        finally:
            logger.info("Shutting down game")
            pygame.quit()
            sys.exit()


def main():
    """Main entry point"""
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
