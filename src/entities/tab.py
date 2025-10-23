"""Tab button UI elements for the Chemination game.

This module contains the TabButton class that represents tab-like buttons
in the game's user interface. It handles button states, visual feedback,
and user interactions.
"""

from typing import Optional

import pygame

from src.utils.tools import create_alpha_image


class TabButton(pygame.sprite.Sprite):
    """Represents a tab-style button UI element.
    
    This class handles tab button rendering, state management, visual feedback,
    and user interaction events. Tabs typically have two states: normal and selected.
    """

    def __init__(self, image_path1: str, image_path2: str, x: int, y: int,
                 width: Optional[int] = None, height: Optional[int] = None,
                 hover_alpha: int = 220, action: Optional[callable] = None):
        """Initialize a tab button with the given parameters.
        
        Args:
            image_path1: Path to the normal state button image.
            image_path2: Path to the selected state button image.
            x:           Button x coordinate.
            y:           Button y coordinate.
            width:       Button width (optional, will scale images if provided).
            height:      Button height (optional, will scale images if provided).
            hover_alpha: Transparency when mouse hovers (0-255).
            action:      Callback function to execute when button is clicked.
        """
        super().__init__()

        # Load and process images
        self.normal_image = pygame.image.load(image_path1).convert_alpha()
        self.click_image = pygame.image.load(image_path2).convert_alpha()

        # Resize images (if dimensions are specified)
        if width and height:
            self.normal_image = pygame.transform.scale(self.normal_image, (width, height))
            self.click_image = pygame.transform.scale(self.click_image, (width, height))

        # Create images for different states
        self.hover_image1 = create_alpha_image(self.normal_image, hover_alpha)
        self.hover_image2 = create_alpha_image(self.click_image, hover_alpha)

        # Set current image
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Button properties
        self.action = action

        # Button states
        self.is_hovered = False
        self.is_clicked = False

    def update_image(self):
        """Update the tab button's image based on its current state.
        
        Selects the appropriate image based on the button's current interaction
        state (normal, hover, clicked/selected).
        """
        if self.is_clicked:
            if self.is_hovered:
                self.image = self.hover_image2
            else:
                self.image = self.click_image
        else:
            self.image = self.normal_image
            if self.is_hovered:
                self.image = self.hover_image1
            else:
                self.image = self.normal_image

    def set_click_status(self, clicked):
        """Set the click/selected status of the tab button.
        
        Args:
            clicked: True to set the button as clicked/selected, False otherwise.
        """
        self.is_clicked = clicked
        self.update_image()

    def update(self, event: pygame.event.Event):
        """Update the tab button's state based on user input events.
        
        Handles mouse hover, click, and release events to provide visual
        feedback and execute the button's action when clicked.
        
        Args:
            event: Pygame event to process.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Handle mouse events.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                if self.action:
                    self.action()

        # Update image
        self.update_image()
