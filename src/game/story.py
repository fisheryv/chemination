import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD
from src.game.scene import Scene
from src.utils.tools import resource_path

story_book = [
    {
        "bg": "story_bg1.jpg",
        "text": ['Legend has it that there is',
                 'a magical kingdom called Chemminos',
                 'on the distant planet Alchelas.']
    },
    {
        "bg": "story_bg2.jpg",
        "text": ['This country advocates chemistry,',
                 'and almost everyone knows',
                 'some chemical knowledge.',
                 'Chemists have brought great benefits',
                 'to the people and are highly respected.']
    },
    {
        "bg": "story_bg3.jpg",
        "text": ["However, the God of the Void, Xel'Naga, ",
                 'opposes all orders in the world.',
                 'He believes that the people of',
                 'Chemminos have mastered too many',
                 'chemical elements and reactions.']
    },
    {
        "bg": "story_bg4.jpg",
        "text": ["So he launched the Infinite Hypnosis",
                 'and sealed all the chemists in Chemminos',
                 'in the Land of Chaos. ',
                 'He also sent out "Elemental Evil Spirits"',
                 'to attack the Kingdom of Chemminos.']
    },
    {
        "bg": "story_bg5.jpg",
        "text": ["In this moment of crisis,",
                 'Commander Lucas Fisher',
                 'organized the people to resist',
                 'the invasion of the evil spirits.',
                 'They used their chemical knowledge',
                 'to defend their homeland......']
    },
]


class StoryScene(Scene):
    """Story scene that displays the game's narrative with animated transitions."""

    def __init__(self, parent):
        """Initialize the story scene.
        
        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)  # Call parent class constructor
        self.background = None  # Background image
        self.story = None
        # Load TTF font file
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 36)
        except FileNotFoundError:
            # If font file does not exist, use system default font
            self.font = pygame.font.SysFont(None, 36)
        self.fade_surface = None
        self.line_surfaces = []
        self.total_text_height = 0
        self.text_block_y = 0
        self.rectangle = None
        self.rect_y = 0
        self.rect_x = 0
        self.step = 0
        self.show_count = 0
        self.fade_progress = 0
        self.status = "FadeIn"
        self.init_story()

    def init_story(self, step: int = 0):
        """Initialize story elements for the given step.
        
        Args:
            step: The index of the story segment to display.
        """
        self.show_count = 0
        self.story = story_book[step]
        bg = resource_path("assets/images/story/" + self.story['bg'])
        # Load background image
        self.background = pygame.image.load(bg)
        self.status = "FadeIn"
        self.line_surfaces = []
        for line in self.story["text"]:
            line_surface = self.font.render(line, True, GOLD)  # White text
            self.line_surfaces.append(line_surface)
        # Calculate total height of text block
        self.total_text_height = sum(surface.get_height() for surface in self.line_surfaces)
        if len(self.line_surfaces) > 1:
            self.total_text_height += (len(self.line_surfaces) - 1) * 5  # Line spacing
            # Vertical center position calculation
            self.text_block_y = (SCREEN_HEIGHT - self.total_text_height) // 2
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Create semi-transparent black rectangle Surface
        rect_height = self.total_text_height + 20
        self.rectangle = pygame.Surface((SCREEN_WIDTH, rect_height), pygame.SRCALPHA)
        self.rectangle.fill((0, 0, 0, 180))  # Semi-transparent black
        self.rect_y = (SCREEN_HEIGHT - rect_height) // 2
        self.rect_x = -SCREEN_WIDTH  # Initial position off-screen to the left

    def next_story(self):
        """Advance to the next story segment or return to main menu if at the end."""
        self.step += 1
        if self.step >= len(story_book):
            self.parent.main_menu()
        else:
            self.init_story(self.step)

    def update(self):
        """Update the story scene animation state."""
        if self.status == "FadeIn":
            self.fade_progress += 5
            if self.fade_progress >= 255:
                self.fade_progress = 255
            self.fade_surface.fill((0, 0, 0, 255 - self.fade_progress))
            if self.fade_progress == 255:
                self.status = "Text"
        elif self.status == "Text":
            # Update rectangle position
            self.rect_x += 20
            if self.rect_x >= 0:
                self.rect_x = 0
                self.status = "Show"
        elif self.status == "Show":
            self.show_count += 1
            if self.show_count >= 180:
                self.status = "FadeOut"
        elif self.status == "FadeOut":
            self.fade_progress -= 5
            if self.fade_progress <= 0:
                self.fade_progress = 0
            self.fade_surface.fill((0, 0, 0, 255 - self.fade_progress))
            if self.fade_progress == 0:
                self.next_story()

    def _render_text(self, screen: pygame.Surface):
        """Render the story text and background rectangle.
        
        Args:
            screen: The pygame surface to render to.
        """
        # Draw rectangle
        screen.blit(self.rectangle, (self.rect_x, self.rect_y))

        # Draw multi-line text (horizontally centered, vertically centered)
        current_y = self.text_block_y
        for line_surface in self.line_surfaces:
            line_x = self.rect_x + (SCREEN_WIDTH - line_surface.get_width()) // 2
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + 5  # 5 pixel line spacing

    def render(self, screen: pygame.Surface):
        """Render story scene animation

        1. Background fade in
        2. A semi-transparent black rectangle flies in from left to right
        3. Rectangle width matches background image width, height is text height + 20, rectangle is vertically centered
        4. Draw text inside the semi-transparent rectangle
        5. After staying for 3 seconds, the entire scene fades out

        Args:
            screen: The pygame surface to render to.
        """
        if self.status == "FadeIn":
            screen.blit(self.background, (0, 0))
            screen.blit(self.fade_surface, (0, 0))
        elif self.status == "Text" or self.status == "Show":
            # Draw background
            screen.blit(self.background, (0, 0))
            self._render_text(screen)
        elif self.status == "FadeOut":
            screen.blit(self.background, (0, 0))
            self._render_text(screen)
            screen.blit(self.fade_surface, (0, 0))

    def process_input(self, event: pygame.event.Event):
        """Process user input events for the story scene.
        
        Args:
            event: The pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.parent.main_menu()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.next_story()
            if event.button == 3:  # Right click
                self.parent.main_menu()