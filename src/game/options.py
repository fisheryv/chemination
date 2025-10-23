import pygame

from src.config.settings import WHITE, get_option, BLACK
from src.entities.button import ImageButton
from src.entities.switcher import Switcher
from src.game.scene import Scene
from src.utils.tools import resource_path

option_text = [
    "Music:",
    "Intro:"
]

WORDS = [
    "A chemist is not a chemist",
    "because he does titrations",
    "or uses a spectrometer, ",
    "but because he thinks",
    "chemically about the world.",
    "         ----Roald Hoffmann",
    "",
    "Chemistry is, well,",
    "chemistry is hell, ",
    "but it opens all the doors",
    "to all the sciences.",
    "         ----George Hammond",
    "",
    "The secret of life, from",
    "the beginning to the end,",
    "is at its core the secret",
    "of chemistry.",
    "         ----Linus Pauling"
]


class OptionsScene(Scene):

    def __init__(self, parent):
        """
        Initialize the operation scene.

        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)  # Call parent class constructor
        self.background = pygame.image.load(resource_path("assets/images/ui/options_bg.jpg"))  # Background image
        try:
            font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 28)
        except FileNotFoundError:
            # If font file does not exist, use system default font
            font = pygame.font.SysFont(None, 28)
        self.line_surfaces = []
        for line in option_text:
            line_surface = font.render(line, True, WHITE)
            self.line_surfaces.append(line_surface)
        try:
            font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 16)
        except FileNotFoundError:
            # If font file does not exist, use system default font
            font = pygame.font.SysFont(None, 16)
        self.words_surfaces = []
        for line in WORDS:
            line_surface = font.render(line, True, BLACK)
            self.words_surfaces.append(line_surface)

        button_width, button_height = 50, 50
        _x, _y = 20, 30
        button_back = ImageButton(resource_path("assets/images/ui/back_arrow.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)
        button_width, button_height = 127, 60
        _x, _y = 850, 150
        _initial_state = get_option("game", "music") == "on"
        music_switcher = Switcher(_x, _y, button_width, button_height, initial_state=_initial_state,
                                  action=self.parent.music_toggle)

        _y += 100
        _initial_state = get_option("game", "intro") == "on"
        intro_switcher = Switcher(_x, _y, button_width, button_height, initial_state=_initial_state,
                                  action=self.parent.intro_toggle)
        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        # Add button to sprite group
        self.all_sprites.add(button_back, music_switcher, intro_switcher)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        """Render the options scene to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        screen.blit(self.background, (0, 0))
        _x, _y = 180, 120
        for line_surface in self.words_surfaces:
            screen.blit(line_surface, (_x, _y))
            _y += line_surface.get_height() + 5
        _x, _y = 830, 160
        for line_surface in self.line_surfaces:
            screen.blit(line_surface, (_x - line_surface.get_width(), _y))
            _y += line_surface.get_height() + 70
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """Process user input events for the options scene.

        Args:
            event: The pygame event to process.
        """
        self.all_sprites.update(event)
