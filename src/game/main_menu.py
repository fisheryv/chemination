"""Main menu scene for the Chemination game.

This module contains the MainMenuScene class that displays the game title,
navigation buttons, and a fire particle effect.
"""

import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.button import ImageButton
from src.game.scene import Scene
from src.utils.effects import FireEffect
from src.utils.tools import resource_path


class MainMenuScene(Scene):
    """Main menu scene that displays the game title and navigation buttons."""

    def __init__(self, parent):
        """Initialize the main menu scene.
        
        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)  # Call parent class constructor
        self.background = pygame.image.load(resource_path("assets/images/ui/menu_bg.jpg"))  # Background image
        self.game_title = pygame.image.load(resource_path("assets/images/ui/game_title.png"))  # Game title image
        self.game_title = pygame.transform.scale(self.game_title, (400, 338))

        # Create fire effect at the center bottom of the screen
        fire_x = SCREEN_WIDTH // 2 + 13
        fire_y = SCREEN_HEIGHT - 170  # Position fire near the fire on bg
        self.fire_effect = FireEffect(fire_x, fire_y, intensity=12)

        button_width = int(270 * 0.6)
        button_height = int(110 * 0.6)
        _x = (SCREEN_WIDTH // 2 - button_width) // 2
        _y = SCREEN_HEIGHT - button_height - 50
        button_credits = ImageButton(resource_path("assets/images/ui/menu_credits.png"),
                                     _x, _y, button_width, button_height,
                                     action=self.parent.credits)
        _x = _x + SCREEN_WIDTH // 4
        button_play = ImageButton(resource_path("assets/images/ui/menu_play.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.battle)
        _x = _x + SCREEN_WIDTH // 4
        button_options = ImageButton(resource_path("assets/images/ui/menu_options.png"),
                                     _x, _y, button_width, button_height,
                                     action=self.parent.options)
        button_width, button_height = 50, 50
        _x, _y = 60, 50

        button_help = ImageButton(resource_path("assets/images/ui/menu_help.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.help)
        _x = SCREEN_WIDTH - button_width - _x
        button_close = ImageButton(resource_path("assets/images/ui/menu_close.png"),
                                   _x, _y, button_width, button_height,
                                   action=self.parent.exit_game)
        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        # Add buttons to sprite group
        self.all_sprites.add(button_play, button_options, button_credits, button_help, button_close)

    def update(self):
        """Update the scene state."""
        # Update fire effect
        self.fire_effect.update()

    def render(self, screen: pygame.Surface):
        """Render the main menu scene to the screen.
        
        Args:
            screen: The pygame surface to render to.
        """
        screen_width, screen_height = screen.get_size()
        screen.blit(self.background, (0, 0))
        # Draw fire effect first (behind the title)
        self.fire_effect.draw(screen)
        screen.blit(self.game_title, ((screen_width - self.game_title.get_width()) // 2, 20))
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """Process user input events.
        
        Args:
            event: The pygame event to process.
        """
        self.all_sprites.update(event)
