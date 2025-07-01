"""
Unit tests for configuration system
"""

import unittest
import tempfile
import os
import json
from snake_game.config import GameConfig


class TestGameConfig(unittest.TestCase):
    """Tests for GameConfig class"""

    def setUp(self):
        """Setup for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.json'
        )
        self.temp_file.close()
        self.temp_path = self.temp_file.name

    def tearDown(self):
        """Cleanup temporary file"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)

    def test_config_creation(self):
        """Test config creation with default values"""
        config = GameConfig()
        self.assertEqual(config.WINDOW_WIDTH, 640)
        self.assertEqual(config.WINDOW_HEIGHT, 480)
        self.assertEqual(config.FPS, 10)
        self.assertFalse(config.WALL_COLLISION)

    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        config = GameConfig()
        config.WALL_COLLISION = True
        config.FPS = 20

        # Save to temp file
        config.save_to_file(self.temp_path)

        # Create new config and load
        new_config = GameConfig()
        new_config.load_from_file(self.temp_path)

        self.assertTrue(new_config.WALL_COLLISION)
        self.assertEqual(new_config.FPS, 20)

    def test_toggle_wall_collision(self):
        """Test wall collision toggle"""
        config = GameConfig()
        original_value = config.WALL_COLLISION

        config.toggle_wall_collision()
        self.assertEqual(config.WALL_COLLISION, not original_value)

        config.toggle_wall_collision()
        self.assertEqual(config.WALL_COLLISION, original_value)

    def test_cycle_fps(self):
        """Test FPS cycling"""
        config = GameConfig()
        config.FPS = 10

        new_fps = config.cycle_fps()
        self.assertNotEqual(new_fps, 10)
        self.assertIn(new_fps, config.get_speed_options())

    def test_invalid_config_values(self):
        """Test validation of invalid configuration values"""
        config = GameConfig()

        with self.assertRaises(ValueError):
            config.update_setting('WINDOW_WIDTH', -100)

        with self.assertRaises(ValueError):
            config.update_setting('FPS', 0)

    def test_grid_properties(self):
        """Test grid calculation properties"""
        config = GameConfig()
        expected_width = config.WINDOW_WIDTH // config.GRID_SIZE
        expected_height = config.WINDOW_HEIGHT // config.GRID_SIZE

        self.assertEqual(config.grid_width, expected_width)
        self.assertEqual(config.grid_height, expected_height)


if __name__ == '__main__':
    unittest.main()
