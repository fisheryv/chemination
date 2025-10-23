import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.button import ImageButton
from src.game.scene import Scene
from src.utils.music import load_background_music
from src.utils.tools import resource_path


class GameOverScene(Scene):
    """Game over scene class"""

    def __init__(self, parent):
        """Initialize game over scene

        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)  # Call parent class constructor
        self.background = pygame.image.load(resource_path("assets/images/ui/gameover_bg.jpg"))  # Background image

        button_width = int(270 * 0.6)
        button_height = int(110 * 0.6)
        _x = (SCREEN_WIDTH - button_width) // 2
        _y = SCREEN_HEIGHT - button_height - 50
        button_continue = ImageButton(resource_path("assets/images/ui/menu_continue.png"),
                                      _x, _y, button_width, button_height,
                                      action=self.parent.main_menu)

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        # Add button to sprite group
        self.all_sprites.add(button_continue)

        # Load background music
        load_background_music("gameover_bgm.mp3")

    def update(self):
        """Update scene state"""
        pass

    def render(self, screen: pygame.Surface):
        """Render the game over scene to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """Process user input events.

        Args:
            event: The pygame event to process.
        """
        self.all_sprites.update(event)
