"""
Input management system for Snake Game
"""

import pygame
from enum import Enum
from typing import Dict, Optional, Set, List
from .game_objects import Direction


class InputAction(Enum):
    """Possible game actions"""

    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE = "pause"
    RESTART = "restart"
    QUIT = "quit"


class InputHandler:
    """Input manager with configurable key mappings"""

    def __init__(self):
        # Default key mappings
        self.key_mappings: Dict[int, InputAction] = {
            # Arrow keys
            pygame.K_UP: InputAction.MOVE_UP,
            pygame.K_DOWN: InputAction.MOVE_DOWN,
            pygame.K_LEFT: InputAction.MOVE_LEFT,
            pygame.K_RIGHT: InputAction.MOVE_RIGHT,
            # WASD keys
            pygame.K_w: InputAction.MOVE_UP,
            pygame.K_s: InputAction.MOVE_DOWN,
            pygame.K_a: InputAction.MOVE_LEFT,
            pygame.K_d: InputAction.MOVE_RIGHT,
            # Control keys
            pygame.K_SPACE: InputAction.PAUSE,
            pygame.K_r: InputAction.RESTART,
            pygame.K_q: InputAction.QUIT,
            pygame.K_ESCAPE: InputAction.QUIT,
        }

        # Movement action to direction mapping
        self.action_to_direction: Dict[InputAction, Direction] = {
            InputAction.MOVE_UP: Direction.UP,
            InputAction.MOVE_DOWN: Direction.DOWN,
            InputAction.MOVE_LEFT: Direction.LEFT,
            InputAction.MOVE_RIGHT: Direction.RIGHT,
        }

        # Track which actions are movement actions
        self.movement_actions = {
            InputAction.MOVE_UP,
            InputAction.MOVE_DOWN,
            InputAction.MOVE_LEFT,
            InputAction.MOVE_RIGHT,
        }

    def get_actions_from_events(
        self, events: List[pygame.event.Event]
    ) -> Set[InputAction]:
        """Convert pygame events to game actions"""
        actions = set()

        for event in events:
            if event.type == pygame.KEYDOWN:
                action = self.key_mappings.get(event.key)
                if action:
                    actions.add(action)

        return actions

    def get_direction_from_action(
        self, action: InputAction
    ) -> Optional[Direction]:
        """Convert action to direction"""
        return self.action_to_direction.get(action)

    def is_movement_action(self, action: InputAction) -> bool:
        """Check if action is a movement action"""
        return action in self.movement_actions

    def add_key_mapping(self, key: int, action: InputAction) -> None:
        """Add custom key mapping"""
        self.key_mappings[key] = action

    def remove_key_mapping(self, key: int) -> None:
        """Remove key mapping"""
        if key in self.key_mappings:
            del self.key_mappings[key]
