"""
Unit tests for input handler
"""

import unittest
import pygame
from src.input_handler import InputHandler, InputAction
from src.game_objects import Direction


class TestInputHandler(unittest.TestCase):
    """Tests for InputHandler class"""

    def setUp(self):
        """Setup for each test"""
        pygame.init()
        self.handler = InputHandler()

    def test_key_mappings_exist(self):
        """Test that all expected key mappings exist"""
        expected_keys = [
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_w,
            pygame.K_s,
            pygame.K_a,
            pygame.K_d,
            pygame.K_SPACE,
            pygame.K_r,
            pygame.K_q,
            pygame.K_ESCAPE,
        ]

        for key in expected_keys:
            self.assertIn(key, self.handler.key_mappings)

    def test_movement_action_detection(self):
        """Test movement action detection"""
        movement_actions = [
            InputAction.MOVE_UP,
            InputAction.MOVE_DOWN,
            InputAction.MOVE_LEFT,
            InputAction.MOVE_RIGHT,
        ]

        for action in movement_actions:
            self.assertTrue(self.handler.is_movement_action(action))

        non_movement_actions = [
            InputAction.PAUSE,
            InputAction.RESTART,
            InputAction.QUIT,
        ]

        for action in non_movement_actions:
            self.assertFalse(self.handler.is_movement_action(action))

    def test_direction_conversion(self):
        """Test action to direction conversion"""
        conversions = [
            (InputAction.MOVE_UP, Direction.UP),
            (InputAction.MOVE_DOWN, Direction.DOWN),
            (InputAction.MOVE_LEFT, Direction.LEFT),
            (InputAction.MOVE_RIGHT, Direction.RIGHT),
        ]

        for action, expected_direction in conversions:
            self.assertEqual(
                self.handler.get_direction_from_action(action),
                expected_direction,
            )

        # Non-movement actions should return None
        self.assertIsNone(
            self.handler.get_direction_from_action(InputAction.PAUSE)
        )

    def test_custom_key_mapping(self):
        """Test adding and removing custom key mappings"""
        # Add custom mapping
        custom_key = pygame.K_x
        self.handler.add_key_mapping(custom_key, InputAction.QUIT)
        self.assertEqual(
            self.handler.key_mappings[custom_key], InputAction.QUIT
        )

        # Remove mapping
        self.handler.remove_key_mapping(custom_key)
        self.assertNotIn(custom_key, self.handler.key_mappings)

        # Removing non-existent key should not raise error
        self.handler.remove_key_mapping(pygame.K_z)  # Should not crash

    def test_event_processing(self):
        """Test processing of pygame events"""
        # Create mock events
        events = [
            type('Event', (), {'type': pygame.KEYDOWN, 'key': pygame.K_UP})(),
            type(
                'Event', (), {'type': pygame.KEYDOWN, 'key': pygame.K_SPACE}
            )(),
            type(
                'Event', (), {'type': pygame.KEYUP, 'key': pygame.K_DOWN}
            )(),  # Should be ignored
        ]

        actions = self.handler.get_actions_from_events(events)

        # Should only process KEYDOWN events
        expected_actions = {InputAction.MOVE_UP, InputAction.PAUSE}
        self.assertEqual(actions, expected_actions)


if __name__ == '__main__':
    unittest.main()
