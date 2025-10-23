import pygame

from src.config.settings import SCREEN_WIDTH, GOLD, WHITE
from src.entities.button import ImageButton
from src.game.scene import Scene
from src.utils.tools import resource_path

credits_text = [
    "Producer", "Fisher, Lucas",
    "Scriptwriter", "Fisher",
    "Programmer", "Fisher, Qwen-Coder-3",
    "Artist", "FLUX, PD_PixelCraft, Qwen-Image, \"Pokémon\", \"Grinsia\"",
    "Music:", "from online sources"
]


class CreditsScene(Scene):
    """Credits scene class"""

    def __init__(self, parent):
        """Initialize credits scene

        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)  # Call parent class constructor
        self.background = pygame.image.load(resource_path("assets/images/ui/credits_bg.jpg"))  # Background image
        try:
            font1 = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 28)
            font2 = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 28)
        except FileNotFoundError:
            # If font file does not exist, use system default font
            font1 = pygame.font.SysFont(None, 28)
            font2 = pygame.font.SysFont(None, 28)
        font1.set_underline(True)
        self.line_surfaces = []
        for i, line in enumerate(credits_text):
            if i % 2 == 0:
                line_surface = font1.render(line, True, GOLD)
            else:
                line_surface = font2.render(line, True, WHITE)
            self.line_surfaces.append(line_surface)

        button_width, button_height = 50, 50
        _x, _y = 20, 30
        button_back = ImageButton(resource_path("assets/images/ui/back_arrow.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        # Add button to sprite group
        self.all_sprites.add(button_back)

    def update(self):
        """Update scene state"""
        pass

    def render(self, screen: pygame.Surface):
        """Render the credits scene to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        screen.blit(self.background, (0, 0))
        current_y = 80
        for i, line_surface in enumerate(self.line_surfaces):
            line_x = (SCREEN_WIDTH - line_surface.get_width()) // 2
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + (10 if i % 2 == 0 else 30)
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """Process user input events.

        Args:
            event: The pygame event to process.
        """
        self.all_sprites.update(event)
