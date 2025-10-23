"""Button UI elements for the Chemination game.

This module contains the ImageButton class that represents clickable buttons
in the game's user interface. It handles button states, visual feedback,
and user interactions.
"""

from typing import Optional

import pygame
import os

from src.config.settings import WHITE
from src.utils.tools import create_alpha_image, resource_path


class ImageButton(pygame.sprite.Sprite):
    """Represents an image-based button with visual feedback.
    
    This class handles button rendering, state management (normal, hover, clicked),
    and user interaction events.
    """

    def __init__(self, image_path: str, x: int, y: int,
                 width: Optional[int] = None, height: Optional[int] = None,
                 text: str = "", text_color: pygame.Color = WHITE, font_size: int = 12,
                 hover_alpha: int = 220, click_alpha: int = 180,
                 click_offset: int = 2, action: Optional[callable] = None):
        """Initialize an image button with the given parameters.
        
        Args:
            image_path:   Path to the button image file.
            x:            Button x coordinate.
            y:            Button y coordinate.
            width:        Button width (optional, will scale image if provided).
            height:       Button height (optional, will scale image if provided).
            text:         Text to display on the button.
            text_color:   Color of the button text.
            font_size:    Size of the button text font.
            hover_alpha:  Transparency when mouse hovers (0-255).
            click_alpha:  Transparency when mouse clicks (0-255).
            click_offset: Number of pixels the button moves down when clicked.
            action:       Callback function to execute when button is clicked.
        """
        super().__init__()

        # Load and process image
        try:
            self.original_image = pygame.image.load(resource_path(image_path)).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load image {image_path}: {e}")
            # Create a default rectangle as substitute
            self.original_image = pygame.Surface((width or 100, height or 30), pygame.SRCALPHA)
            self.original_image.fill((100, 100, 100, 200))

        # Resize image (if dimensions are specified)
        if width and height:
            self.original_image = pygame.transform.scale(self.original_image, (width, height))

        # Create images for different states
        self.normal_image = self.original_image.copy()
        self.hover_image = create_alpha_image(self.original_image, hover_alpha)
        self.click_image = create_alpha_image(self.original_image, click_alpha)

        # Set current image and position
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Button properties
        self.text = text
        self.text_color = text_color
        self.click_offset = click_offset
        self.action = action

        # Button states
        self.is_hovered = False
        self.is_clicked = False
        self.normal_position = (x, y)
        self.clicked_position = (x + click_offset, y + click_offset)

        # Render text (if any)
        if self.text:
            self._render_text(font_size)

    def _render_text(self, font_size: int):
        """Render button text onto all button states.
        
        Loads a custom font if available, otherwise falls back to system default.
        Renders the text onto all button state images (normal, hover, click).
        
        Args:
            font_size: Size of the font to use for rendering text.
        """
        # Load TTF font file
        try:
            font_path = resource_path("assets/fonts/PixelEmulator.ttf")
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, font_size)
            else:
                raise FileNotFoundError("Font file does not exist")
        except (FileNotFoundError, pygame.error):
            # If font file does not exist, use system default font
            font = pygame.font.SysFont(None, font_size)

        self.text_surf = font.render(self.text, True, self.text_color)
        text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Draw text onto button images
        self.normal_image.blit(self.text_surf, text_rect)
        self.hover_image.blit(self.text_surf, text_rect)
        self.click_image.blit(self.text_surf, text_rect)

    def update_image(self):
        """Update the button's image based on its current state.
        
        Selects the appropriate image (normal, hover, or click) based on
        the button's current interaction state.
        """
        if self.is_clicked:
            self.image = self.click_image
        elif self.is_hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image

    def update(self, event: pygame.event.Event):
        """Update the button's state based on user input events.
        
        Handles mouse hover, click, and release events to provide visual
        feedback and execute the button's action when clicked.
        
        Args:
            event: Pygame event to process.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.image = self.click_image
                self.rect.topleft = self.clicked_position

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered and self.action:
                self.action()
            self.is_clicked = False
            self.rect.topleft = self.normal_position

        # Update image
        self.update_image()
