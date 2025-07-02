"""
Menu system for Snake Game
"""

import pygame
from enum import Enum
from typing import List, Optional
from .config import CONFIG, COLORS
from .high_score import HighScoreManager
from .logger import logger


class MenuState(Enum):
    """Menu state enumeration"""

    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    HIGH_SCORES = "high_scores"
    GAME = "game"
    QUIT = "quit"


class BaseMenu:
    """Base class for all menus"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 72)
        self.selected_item = 0
        self.menu_items: List[str] = []

        # Menu colors
        self.selected_color = COLORS.BLUE
        self.normal_color = COLORS.WHITE
        self.title_color = COLORS.GREEN
        self.background_color = COLORS.BLACK

    def handle_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle menu input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_item = (self.selected_item - 1) % len(
                    self.menu_items
                )
                logger.debug(f"Menu selection: {self.selected_item}")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_item = (self.selected_item + 1) % len(
                    self.menu_items
                )
                logger.debug(f"Menu selection: {self.selected_item}")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._handle_selection()
            elif event.key == pygame.K_ESCAPE:
                return self._handle_escape()
        return None

    def _handle_selection(self) -> Optional[str]:
        """Handle menu item selection - to be overridden by subclasses"""
        return None

    def _handle_escape(self) -> Optional[str]:
        """Handle escape key - to be overridden by subclasses"""
        return None

    def draw_title(self, title: str, y_offset: int = 50) -> None:
        """Draw menu title"""
        title_surface = self.title_font.render(title, True, self.title_color)
        title_rect = title_surface.get_rect(
            center=(CONFIG.WINDOW_WIDTH // 2, y_offset)
        )
        self.screen.blit(title_surface, title_rect)

    def draw_menu_items(self, start_y: int = 200, spacing: int = 60) -> None:
        """Draw menu items"""
        for i, item in enumerate(self.menu_items):
            color = (
                self.selected_color
                if i == self.selected_item
                else self.normal_color
            )
            item_surface = self.font.render(item, True, color)
            item_rect = item_surface.get_rect(
                center=(CONFIG.WINDOW_WIDTH // 2, start_y + i * spacing)
            )
            self.screen.blit(item_surface, item_rect)

    def draw_background(self) -> None:
        """Draw menu background"""
        self.screen.fill(self.background_color)

        # Draw decorative border
        pygame.draw.rect(
            self.screen,
            COLORS.DARK_GREEN,
            (10, 10, CONFIG.WINDOW_WIDTH - 20, CONFIG.WINDOW_HEIGHT - 20),
            3,
        )

    def draw(self) -> None:
        """Draw the menu - to be overridden by subclasses"""
        self.draw_background()


class MainMenu(BaseMenu):
    """Main menu for the Snake game"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.menu_items = ["Start Game", "Settings", "High Scores", "Quit"]

    def _handle_selection(self) -> str:
        """Handle main menu selection"""
        if self.selected_item == 0:  # Start Game
            logger.info("Starting new game")
            return MenuState.GAME.value
        elif self.selected_item == 1:  # Settings
            logger.info("Opening settings")
            return MenuState.SETTINGS.value
        elif self.selected_item == 2:  # High Scores
            logger.info("Opening high scores")
            return MenuState.HIGH_SCORES.value
        elif self.selected_item == 3:  # Quit
            logger.info("Quitting game")
            return MenuState.QUIT.value
        return MenuState.MAIN_MENU.value

    def _handle_escape(self) -> str:
        """Handle escape key in main menu"""
        return MenuState.QUIT.value

    def draw(self) -> None:
        """Draw main menu"""
        self.draw_background()
        self.draw_title("SNAKE GAME")
        self.draw_menu_items()

        # Draw instructions
        instruction_text = "Use ARROW KEYS or WASD to navigate, ENTER to select"
        instruction_surface = self.small_font.render(
            instruction_text, True, COLORS.GRAY
        )
        instruction_rect = instruction_surface.get_rect(
            center=(CONFIG.WINDOW_WIDTH // 2, CONFIG.WINDOW_HEIGHT - 30)
        )
        self.screen.blit(instruction_surface, instruction_rect)


class SettingsMenu(BaseMenu):
    """Settings menu for game configuration"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self._update_menu_items()

    def _update_menu_items(self) -> None:
        """Update menu items with current settings"""
        self.menu_items = [
            f"Wall Collision: {'ON' if CONFIG.WALL_COLLISION else 'OFF'}",
            f"Game Speed: {CONFIG.FPS}",
            "Reset to Defaults",  # New option
            "Back to Main Menu",
        ]

    def _handle_selection(self) -> str:
        """Handle settings menu selection"""
        if self.selected_item == 0:  # Toggle wall collision
            self._toggle_wall_collision()
        elif self.selected_item == 1:  # Adjust speed
            self._adjust_speed()
        elif self.selected_item == 2:  # Reset to defaults
            self._reset_to_defaults()
        elif self.selected_item == 3:  # Back to main menu
            return MenuState.MAIN_MENU.value
        return MenuState.SETTINGS.value

    def _reset_to_defaults(self) -> None:
        """Reset all settings to default values"""
        CONFIG.reset_to_defaults()
        CONFIG.save_to_file()
        self._update_menu_items()
        logger.info("Settings reset to defaults")

    def _handle_escape(self) -> str:
        """Handle escape key in settings"""
        return MenuState.MAIN_MENU.value

    def _toggle_wall_collision(self) -> None:
        """Toggle wall collision setting"""
        CONFIG.toggle_wall_collision()
        self._update_menu_items()
        # Save configuration
        CONFIG.save_to_file()
        logger.info(f"Wall collision set to: {CONFIG.WALL_COLLISION}")

    def _adjust_speed(self) -> None:
        """Cycle through different speed options"""
        new_fps = CONFIG.cycle_fps()
        self._update_menu_items()
        # Save configuration
        CONFIG.save_to_file()
        logger.info(f"Game speed set to: {new_fps}")

    def draw(self) -> None:
        """Draw settings menu"""
        self.draw_background()
        self.draw_title("SETTINGS", 80)
        self.draw_menu_items(200, 60)  # Reduced spacing for 4 items

        # Draw settings description
        descriptions = [
            "Toggle wall collision on/off",
            "Adjust game speed (5-30 FPS)",
            "Reset all settings to defaults",
            "Return to main menu",
        ]

        if self.selected_item < len(descriptions):
            desc_surface = self.small_font.render(
                descriptions[self.selected_item], True, COLORS.GRAY
            )
            desc_rect = desc_surface.get_rect(
                center=(CONFIG.WINDOW_WIDTH // 2, 420)
            )
            self.screen.blit(desc_surface, desc_rect)


class HighScoreMenu(BaseMenu):
    """High score display menu"""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.high_score_manager = HighScoreManager()
        self.menu_items = ["Back to Main Menu"]

    def _handle_selection(self) -> str:
        """Handle high score menu selection"""
        if self.selected_item == 0:  # Back to main menu
            return MenuState.MAIN_MENU.value
        return MenuState.HIGH_SCORES.value

    def _handle_escape(self) -> str:
        """Handle escape key in high scores"""
        return MenuState.MAIN_MENU.value

    def draw(self) -> None:
        """Draw high score menu"""
        self.draw_background()
        self.draw_title("HIGH SCORES", 50)

        # Get top scores
        top_scores = self.high_score_manager.get_top_scores(10)

        if not top_scores:
            # No scores yet
            no_scores_text = "No high scores yet!"
            no_scores_surface = self.font.render(
                no_scores_text, True, COLORS.GRAY
            )
            no_scores_rect = no_scores_surface.get_rect(
                center=(CONFIG.WINDOW_WIDTH // 2, 200)
            )
            self.screen.blit(no_scores_surface, no_scores_rect)
        else:
            # Display scores
            start_y = 150
            for i, score_entry in enumerate(top_scores):
                rank = i + 1
                score = score_entry["score"]
                player = score_entry["player"]
                date = score_entry["date"][:10]  # Just the date part

                # Format score line
                score_text = f"{rank:2d}. {score:4d} pts - {player} ({date})"

                # Highlight top 3
                if rank <= 3:
                    color = [COLORS.BLUE, COLORS.GREEN, COLORS.RED][rank - 1]
                else:
                    color = COLORS.WHITE

                score_surface = self.small_font.render(score_text, True, color)
                score_rect = score_surface.get_rect(
                    center=(CONFIG.WINDOW_WIDTH // 2, start_y + i * 25)
                )
                self.screen.blit(score_surface, score_rect)

        # Draw back button
        self.draw_menu_items(CONFIG.WINDOW_HEIGHT - 80, 60)


class MenuManager:
    """Manages menu navigation and state"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Initialize menus
        self.main_menu = MainMenu(screen)
        self.settings_menu = SettingsMenu(screen)
        self.high_score_menu = HighScoreMenu(screen)

        # Current state
        self.current_state = MenuState.MAIN_MENU
        self.running = True

        logger.info("Menu manager initialized")

    def get_current_menu(self) -> BaseMenu:
        """Get the current active menu"""
        if self.current_state == MenuState.MAIN_MENU:
            return self.main_menu
        elif self.current_state == MenuState.SETTINGS:
            return self.settings_menu
        elif self.current_state == MenuState.HIGH_SCORES:
            return self.high_score_menu
        else:
            return self.main_menu

    def handle_events(self) -> Optional[str]:
        """Handle menu events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return MenuState.QUIT.value

            current_menu = self.get_current_menu()
            result = current_menu.handle_input(event)

            if result:
                if result == MenuState.QUIT.value:
                    self.running = False
                    return result
                elif result == MenuState.GAME.value:
                    return result
                else:
                    # Change menu state
                    try:
                        self.current_state = MenuState(result)
                        logger.debug(
                            f"Menu state changed to: {self.current_state}"
                        )
                    except ValueError:
                        logger.warning(f"Invalid menu state: {result}")

        return None

    def update(self) -> None:
        """Update menu logic"""
        # Menus are mostly static, but could add animations here

    def draw(self) -> None:
        """Draw current menu"""
        current_menu = self.get_current_menu()
        current_menu.draw()
        pygame.display.flip()

    def run(self) -> str:
        """Run the menu system and return next state"""
        logger.info("Starting menu system")

        while self.running:
            result = self.handle_events()
            if result:
                return result

            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth menu navigation

        return MenuState.QUIT.value


def main():
    """Main function for testing menus standalone"""
    pygame.init()
    screen = pygame.display.set_mode(
        (CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Snake Game - Menu")

    menu_manager = MenuManager(screen)
    result = menu_manager.run()

    pygame.quit()
    logger.info(f"Menu system exited with state: {result}")


if __name__ == "__main__":
    main()
