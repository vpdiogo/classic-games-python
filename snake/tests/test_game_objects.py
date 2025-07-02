"""
Unit tests for game objects
"""

import unittest
import pygame
from snake_game.game_objects import Position, Direction, Snake, Food
from snake_game.config import CONFIG


class TestPosition(unittest.TestCase):
    """Tests for Position class"""

    def test_position_creation(self):
        """Test position creation"""
        pos = Position(5, 10)
        self.assertEqual(pos.x, 5)
        self.assertEqual(pos.y, 10)

    def test_position_equality(self):
        """Test position equality comparison"""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        pos3 = Position(3, 10)

        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)
        self.assertNotEqual(pos1, "not a position")

    def test_position_hashing(self):
        """Test position can be used in sets"""
        pos1 = Position(5, 10)
        pos2 = Position(5, 10)
        pos3 = Position(3, 10)

        positions = {pos1, pos2, pos3}
        self.assertEqual(len(positions), 2)  # pos1 and pos2 are the same

    def test_position_addition_with_direction(self):
        """Test adding direction to position"""
        pos = Position(5, 5)

        # Test all directions
        self.assertEqual(pos + Direction.RIGHT, Position(6, 5))
        self.assertEqual(pos + Direction.LEFT, Position(4, 5))
        self.assertEqual(pos + Direction.UP, Position(5, 4))
        self.assertEqual(pos + Direction.DOWN, Position(5, 6))

    def test_to_pixel_conversion(self):
        """Test grid to pixel conversion"""
        pos = Position(2, 3)
        pixels = pos.to_pixel()

        expected = (2 * CONFIG.GRID_SIZE, 3 * CONFIG.GRID_SIZE)
        self.assertEqual(pixels, expected)

    def test_position_boundary_detection(self):
        """Test position boundary detection"""
        # Test out of bounds positions
        self.assertTrue(Position(-1, 5).is_out_of_bounds())
        self.assertTrue(Position(CONFIG.grid_width, 5).is_out_of_bounds())
        self.assertTrue(Position(5, -1).is_out_of_bounds())
        self.assertTrue(Position(5, CONFIG.grid_height).is_out_of_bounds())

        # Test valid positions
        self.assertFalse(Position(0, 0).is_out_of_bounds())
        self.assertFalse(
            Position(
                CONFIG.grid_width - 1, CONFIG.grid_height - 1
            ).is_out_of_bounds()
        )
        self.assertFalse(Position(5, 5).is_out_of_bounds())

    def test_distance_to(self):
        """Test Manhattan distance calculation"""
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)

        self.assertEqual(pos1.distance_to(pos2), 7)  # 3 + 4
        self.assertEqual(pos2.distance_to(pos1), 7)  # Distance is symmetric

    def test_repr(self):
        """Test string representation"""
        pos = Position(5, 10)
        self.assertEqual(repr(pos), "Position(5, 10)")

    def test_position_wrap_around(self):
        """Test position wrap around at boundaries"""
        # Test wrapping at right edge
        pos = Position(CONFIG.grid_width, 5)
        wrapped = pos.wrap_around()
        self.assertEqual(wrapped, Position(0, 5))

        # Test wrapping at left edge
        pos = Position(-1, 5)
        wrapped = pos.wrap_around()
        self.assertEqual(wrapped, Position(CONFIG.grid_width - 1, 5))

        # Test wrapping at bottom edge
        pos = Position(5, CONFIG.grid_height)
        wrapped = pos.wrap_around()
        self.assertEqual(wrapped, Position(5, 0))

        # Test wrapping at top edge
        pos = Position(5, -1)
        wrapped = pos.wrap_around()
        self.assertEqual(wrapped, Position(5, CONFIG.grid_height - 1))

        # Test no wrapping for valid positions
        pos = Position(5, 5)
        wrapped = pos.wrap_around()
        self.assertEqual(wrapped, Position(5, 5))


class TestSnake(unittest.TestCase):
    """Tests for Snake class"""

    def setUp(self):
        """Setup for each test"""
        pygame.init()  # Required for pygame functionality
        # Store original wall collision setting
        self.original_wall_collision = CONFIG.WALL_COLLISION
        self.snake = Snake()

    def tearDown(self):
        """Restore original configuration after each test"""
        CONFIG.WALL_COLLISION = self.original_wall_collision

    def test_snake_initial_state(self):
        """Test snake initial state"""
        self.assertEqual(len(self.snake.body), CONFIG.INITIAL_SNAKE_LENGTH)
        self.assertEqual(self.snake.direction, Direction.RIGHT)
        self.assertEqual(self.snake.next_direction, Direction.RIGHT)
        self.assertFalse(self.snake.grow_pending)

    def test_snake_initial_position(self):
        """Test snake starts at center"""
        head = self.snake.body[0]
        self.assertEqual(head.x, CONFIG.center_x)
        self.assertEqual(head.y, CONFIG.center_y)

    def test_snake_movement(self):
        """Test basic snake movement"""
        initial_head = self.snake.body[0]
        initial_length = len(self.snake.body)

        self.snake.move()

        new_head = self.snake.body[0]
        self.assertEqual(new_head.x, initial_head.x + 1)  # Moved right
        self.assertEqual(new_head.y, initial_head.y)
        self.assertEqual(
            len(self.snake.body), initial_length
        )  # Length unchanged

    def test_snake_growth(self):
        """Test snake growth mechanism"""
        initial_length = len(self.snake.body)

        self.snake.grow()
        self.assertTrue(self.snake.grow_pending)

        self.snake.move()
        self.assertEqual(len(self.snake.body), initial_length + 1)
        self.assertFalse(self.snake.grow_pending)

    def test_valid_direction_changes(self):
        """Test valid direction changes"""
        # From RIGHT, can go UP or DOWN
        self.assertTrue(self.snake.change_direction(Direction.UP))
        self.assertEqual(self.snake.next_direction, Direction.UP)

        self.assertTrue(self.snake.change_direction(Direction.DOWN))
        self.assertEqual(self.snake.next_direction, Direction.DOWN)

    def test_invalid_direction_changes(self):
        """Test invalid (reverse) direction changes"""
        # From RIGHT, cannot go LEFT
        self.snake.direction = Direction.RIGHT
        self.assertFalse(self.snake.change_direction(Direction.LEFT))
        self.assertEqual(
            self.snake.next_direction, Direction.RIGHT
        )  # Unchanged

        # From UP, cannot go DOWN
        self.snake.direction = Direction.UP
        self.assertFalse(self.snake.change_direction(Direction.DOWN))

    def test_wall_collision_enabled(self):
        """Test that wall collision works when enabled"""
        CONFIG.WALL_COLLISION = True
        snake = Snake()
        snake.body[0] = Position(-1, 5)
        self.assertTrue(
            snake.check_collision(), "Should collide with wall when enabled"
        )

    def test_wall_collision_disabled(self):
        """Test that wall collision is disabled when configured"""
        CONFIG.WALL_COLLISION = False
        snake = Snake()
        snake.body[0] = Position(-1, 5)
        self.assertFalse(
            snake.check_collision(),
            "Should not collide with wall when disabled",
        )

    def test_wrap_around_when_wall_collision_disabled(self):
        """Test wrap-around behavior when wall collision is disabled"""
        CONFIG.WALL_COLLISION = False
        snake = Snake()

        # Test wrapping from right to left
        snake.body[0] = Position(CONFIG.grid_width - 1, 5)
        snake.direction = Direction.RIGHT
        snake.next_direction = Direction.RIGHT

        snake.move()

        # Head should wrap to left side
        self.assertEqual(snake.body[0], Position(0, 5))

    def test_snake_wrap_around_movement(self):
        """Test snake wraps around when hitting boundaries"""
        CONFIG.WALL_COLLISION = False
        snake = Snake()

        # Test wrapping from right to left
        snake.body[0] = Position(CONFIG.grid_width - 1, 5)
        snake.direction = Direction.RIGHT
        snake.next_direction = Direction.RIGHT

        snake.move()

        # Head should wrap to left side
        self.assertEqual(snake.body[0], Position(0, 5))

        # Test wrapping from bottom to top
        snake.body[0] = Position(5, CONFIG.grid_height - 1)
        snake.direction = Direction.DOWN
        snake.next_direction = Direction.DOWN

        snake.move()

        # Head should wrap to top
        self.assertEqual(snake.body[0], Position(5, 0))

    def test_collision_with_self(self):
        """Test self-collision detection"""
        # Create a snake that intersects with itself
        self.snake.body = [
            Position(5, 5),  # Head
            Position(4, 5),
            Position(3, 5),
            Position(3, 4),
            Position(4, 4),
            Position(5, 4),
            Position(5, 5),  # Same as head
        ]

        self.assertTrue(self.snake.check_collision())

    def test_no_collision(self):
        """Test no collision in normal state"""
        # Fresh snake shouldn't have any collisions
        self.assertFalse(self.snake.check_collision())

    def test_ate_food(self):
        """Test food eating detection"""
        food = Food()

        # Place food at snake's head position
        food.position = self.snake.body[0]
        self.assertTrue(self.snake.ate_food(food))

        # Place food elsewhere
        food.position = Position(0, 0)
        self.assertFalse(self.snake.ate_food(food))

    def test_get_length(self):
        """Test length getter"""
        self.assertEqual(self.snake.get_length(), CONFIG.INITIAL_SNAKE_LENGTH)

        self.snake.grow()
        self.snake.move()
        self.assertEqual(
            self.snake.get_length(), CONFIG.INITIAL_SNAKE_LENGTH + 1
        )


class TestFood(unittest.TestCase):
    """Tests for Food class"""

    def setUp(self):
        """Setup for each test"""
        pygame.init()
        self.food = Food()

    def test_food_creation(self):
        """Test food is created with valid position"""
        self.assertIsInstance(self.food.position, Position)
        # Food should be within bounds (not out of bounds)
        self.assertFalse(self.food.position.is_out_of_bounds())

    def test_food_respawn_avoids_snake(self):
        """Test food respawns avoiding snake positions"""
        # Create snake positions that cover most of the grid
        snake_positions = []
        for x in range(min(5, CONFIG.grid_width)):
            for y in range(min(5, CONFIG.grid_height)):
                snake_positions.append(Position(x, y))

        self.food.respawn(snake_positions)

        # Food should not be in any snake position
        self.assertNotIn(self.food.position, snake_positions)
        # Food should be within bounds (not out of bounds)
        self.assertFalse(self.food.position.is_out_of_bounds())

    def test_food_respawn_fallback(self):
        """Test food respawn with fallback when most positions are taken"""
        # Create extensive snake positions leaving only a few spots
        snake_positions = []
        for x in range(CONFIG.grid_width):
            for y in range(CONFIG.grid_height):
                if not (
                    x == CONFIG.grid_width - 1 and y == CONFIG.grid_height - 1
                ):
                    snake_positions.append(Position(x, y))

        self.food.respawn(snake_positions)

        # Should find the one remaining position
        expected_position = Position(
            CONFIG.grid_width - 1, CONFIG.grid_height - 1
        )
        self.assertEqual(self.food.position, expected_position)


if __name__ == "__main__":
    unittest.main()
