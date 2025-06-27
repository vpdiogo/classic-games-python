import pygame
import sys
from enum import Enum
from typing import List, Tuple

# Game settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255)

# FPS
FPS = 10


class Direction(Enum):
    """Enum for the possible directions of the snake"""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Position:
    """Class to represent a position on the grid"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, direction: Direction):
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

    def to_pixel(self) -> Tuple[int, int]:
        """Converts grid position to pixels"""
        return (self.x * GRID_SIZE, self.y * GRID_SIZE)


class Food:
    """Class to represent the food"""

    def __init__(self):
        self.position = self._generate_position()

    def _generate_position(self) -> Position:
        """Generates a random position for the food"""
        import random

        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return Position(x, y)

    def respawn(self, snake_positions: List[Position]):
        """Respawns the food avoiding the snake"""
        while True:
            self.position = self._generate_position()
            if self.position not in snake_positions:
                break

    def draw(self, screen: pygame.Surface):
        """Draws the food on the screen"""
        pixel_pos = self.position.to_pixel()
        pygame.draw.rect(
            screen, RED, (pixel_pos[0], pixel_pos[1], GRID_SIZE, GRID_SIZE)
        )


class Snake:
    """Class to represent the snake"""

    def __init__(self):
        # Initial position at the center of the screen
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2

        self.body = [
            Position(center_x, center_y),
            Position(center_x - 1, center_y),
            Position(center_x - 2, center_y),
        ]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT # Buffer for direction changes
        self.grow_pending = False

    def move(self):
        """Moves the snake one position in the current direction"""
        # Update direction if a new one is set
        self.direction = self.next_direction

        # Calculate new head position
        new_head = self.body[0] + self.direction

        # Add new head
        self.body.insert(0, new_head)

        # Remove the tail if not growing
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def change_direction(self, new_direction: Direction):
        """Changes the snake's direction (prevents reverse movement)"""
        # Prevent the snake from moving in the opposite direction
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction

    def grow(self):
        """Marks that the snake should grow on the next move"""
        self.grow_pending = True

    def check_collision(self) -> bool:
        """Checks if the snake has collided with the borders or with itself"""
        head = self.body[0]

        # Collision with borders
        if (
            head.x < 0
            or head.x >= GRID_WIDTH
            or head.y < 0
            or head.y >= GRID_HEIGHT
        ):
            return True

        # Collision with the snake's own body
        if head in self.body[1:]:
            return True

        return False

    def ate_food(self, food: Food) -> bool:
        """Checks if the snake has eaten the food"""
        return self.body[0] == food.position

    def draw(self, screen: pygame.Surface):
        """Draws the snake on the screen"""
        for i, segment in enumerate(self.body):
            pixel_pos = segment.to_pixel()
            # Head in a different color
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(
                screen,
                color,
                (pixel_pos[0], pixel_pos[1], GRID_SIZE, GRID_SIZE),
            )
            # Border for better visualization
            pygame.draw.rect(
                screen,
                BLACK,
                (pixel_pos[0], pixel_pos[1], GRID_SIZE, GRID_SIZE),
                1,
            )


class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.reset_game()

    def reset_game(self):
        """Resets the game"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.direction_changed_this_frame = False

        # Ensure that food does not spawn on the snake
        self.food.respawn(self.snake.body)

    def handle_events(self):
        """Handles pygame events"""
        # Reset the flag at the start of each frame
        self.direction_changed_this_frame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                else:
                    # Movement controls - only 1 per frame
                    if not self.direction_changed_this_frame:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.change_direction(Direction.UP)
                            self.direction_changed_this_frame = True
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.change_direction(Direction.DOWN)
                            self.direction_changed_this_frame = True
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.change_direction(Direction.LEFT)
                            self.direction_changed_this_frame = True
                        elif (
                            event.key == pygame.K_RIGHT or event.key == pygame.K_d
                        ):
                            self.snake.change_direction(Direction.RIGHT)
                            self.direction_changed_this_frame = True
                    
                    if event.key == pygame.K_SPACE:
                        was_paused = self.paused
                        self.paused = not self.paused
                        
                        # Clear the buffer when exiting pause
                        if was_paused and not self.paused:
                            self.snake.next_direction = self.snake.direction
                            
                    elif event.key == pygame.K_r:
                        self.reset_game()

        return True

    def update(self):
        """Updates the game logic"""
        if self.game_over or self.paused:
            return

        # Move the snake
        self.snake.move()

        # Check collisions
        if self.snake.check_collision():
            self.game_over = True
            return

        # Check if ate food
        if self.snake.ate_food(self.food):
            self.snake.grow()
            self.score += 10
            self.food.respawn(self.snake.body)

    def draw_text(self, text: str, x: int, y: int, color=WHITE):
        """Draws text on the screen"""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        """Draws all elements on the screen"""
        # Clear the screen
        self.screen.fill(BLACK)

        if not self.game_over:
            # Desenha a cobra e a comida
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

        # Draw the score
        self.draw_text(f"Score: {self.score}", 10, 10)

        # Draw status messages
        if self.paused:
            self.draw_text(
                "PAUSED", WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, BLUE
            )
            self.draw_text(
                "Press SPACE to continue",
                WINDOW_WIDTH // 2 - 120,
                WINDOW_HEIGHT // 2 + 40,
            )

        elif self.game_over:
            self.draw_text(
                "GAME OVER",
                WINDOW_WIDTH // 2 - 80,
                WINDOW_HEIGHT // 2 - 40,
                RED,
            )
            self.draw_text(
                f"Final Score: {self.score}",
                WINDOW_WIDTH // 2 - 80,
                WINDOW_HEIGHT // 2,
            )
            self.draw_text(
                "Press R to restart or Q to quit",
                WINDOW_WIDTH // 2 - 150,
                WINDOW_HEIGHT // 2 + 40,
            )

        # Update the screen
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Main function"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
