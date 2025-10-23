"""Toggle switch UI elements for the Chemination game.

This module contains the Switcher class that represents toggle switches
in the game's user interface. It handles switch states, visual feedback,
and user interactions.
"""

from typing import Optional

import pygame

from src.utils.tools import create_alpha_image, resource_path


class Switcher(pygame.sprite.Sprite):
    """Represents a toggle switch UI element.
    
    This class handles switch rendering, state management (on/off),
    visual feedback, and user interaction events.
    """

    def __init__(self, x: int, y: int,
                 width: Optional[int] = None, height: Optional[int] = None,
                 initial_state: bool = False,
                 hover_alpha: int = 220, click_alpha: int = 180,
                 action: Optional[callable] = None):
        """Initialize a toggle switch with the given parameters.
        
        Args:
            x:             Switch x coordinate.
            y:             Switch y coordinate.
            width:         Switch width (optional, will scale images if provided).
            height:        Switch height (optional, will scale images if provided).
            initial_state: Initial state (True for on, False for off).
            hover_alpha:   Transparency when mouse hovers (0-255).
            click_alpha:   Transparency when mouse clicks (0-255).
            action:        Callback function to execute when state changes.
        """
        super().__init__()

        # Load and process images
        self.image: Optional[pygame.Surface] = None
        self.original_image_on = pygame.image.load(resource_path("assets/images/ui/switcher_on.png")).convert_alpha()
        self.original_image_off = pygame.image.load(resource_path("assets/images/ui/switcher_off.png")).convert_alpha()

        # Resize images (if dimensions are specified)
        if width and height:
            self.original_image_on = pygame.transform.scale(self.original_image_on, (width, height))
            self.original_image_off = pygame.transform.scale(self.original_image_off, (width, height))

        # Create images for different states
        self.normal_image_on = self.original_image_on.copy()
        self.hover_image_on = create_alpha_image(self.original_image_on, hover_alpha)
        self.click_image_on = create_alpha_image(self.original_image_on, click_alpha)

        self.normal_image_off = self.original_image_off.copy()
        self.hover_image_off = create_alpha_image(self.original_image_off, hover_alpha)
        self.click_image_off = create_alpha_image(self.original_image_off, click_alpha)

        self.normal_image = None
        self.hover_image = None
        self.click_image = None

        # Button states
        self.is_hovered = False
        self.is_clicked = False
        self.normal_position = (x, y)

        # Set current state and image
        self.state = initial_state
        self.update_image()

        self.rect = self.image.get_rect(topleft=(x, y))

        # Button click action
        self.action = action

    def update_image(self):
        """Update the switch's image based on its current state.
        
        Selects the appropriate image (on/off) based on the switch's current state
        and interaction state (normal, hover, click).
        """
        if self.state:  # On state
            self.normal_image = self.normal_image_on
            self.hover_image = self.hover_image_on
            self.click_image = self.click_image_on
        else:  # Off state
            self.normal_image = self.normal_image_off
            self.hover_image = self.hover_image_off
            self.click_image = self.click_image_off

        # Set current image
        if self.is_clicked:
            self.image = self.click_image
        elif self.is_hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image

    def update(self, event: pygame.event.Event):
        """Update the switch's state based on user input events.
        
        Handles mouse hover, click, and release events to provide visual
        feedback and toggle the switch state when clicked.
        
        Args:
            event: Pygame event to process.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.rect.topleft = self.normal_position

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                # Toggle state
                self.state = not self.state
                if self.action:
                    self.action(self.state)

            self.is_clicked = False
            self.rect.topleft = self.normal_position

        # Update image
        self.update_image()

    def get_state(self) -> bool:
        """Get the current state of the switch.
        
        Returns:
            bool: Current state (True for on, False for off).
        """
        return self.state

    def set_state(self, state: bool):
        """Set the state of the switch and update its appearance.
        
        Args:
            state: New state (True for on, False for off).
        """
        self.state = state
        self.update_image()
