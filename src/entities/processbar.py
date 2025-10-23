"""Progress bar UI component for the Chemination game.

This module contains the ProcessBar class that represents a customizable
progress bar with optional icons, used for displaying health, mana, and
other game metrics.
"""

from typing import Optional

import pygame
from src.utils.tools import resource_path


class ProcessBar:
    """Represents a progress bar UI component.
    
    This class handles the rendering of progress bars with customizable colors,
    sizes, and optional icons. Used for health bars, mana bars, etc.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 border_color: pygame.Color, bg_color: pygame.Color,
                 icon: Optional[str] = None):
        """Initialize a progress bar with the given parameters.
        
        Args:
            x:            X coordinate of the progress bar.
            y:            Y coordinate of the progress bar.
            width:        Width of the progress bar.
            height:       Height of the progress bar.
            border_color: Color of the progress bar border.
            bg_color:     Background color of the progress bar.
            icon:         Optional icon filename to display next to the bar.
        """
        self.x_offset = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_color = border_color
        self.bg_color = bg_color
        self.icon = icon
        if self.icon:
            self.icon = pygame.image.load(resource_path("assets/images/ui/" + self.icon))
            self.icon = pygame.transform.scale(self.icon, (self.height, self.height))
            self.x_offset = self.height + 10
        self.progress = 100
        self.size = self.height // 6
        self.bar_w = self.width - self.x_offset - self.size * 6
        self.bar_x = self.x + self.size * 3
        self.bar_y = self.y + self.size * 2
        self.bar_h = self.size * 2

    def set_progress(self, progress: int):
        """Set the progress value and update the bar width.
        
        Args:
            progress: Progress value (0-100).
        """
        if progress < 0:
            self.progress = 0
        elif progress > 100:
            self.progress = 100
        else:
            self.progress = progress
        self.bar_w = (self.width - self.x_offset - self.size * 6) * self.progress / 100

    def get_progress(self) -> int:
        """Get the current progress value.
        
        Returns:
            int: Current progress value (0-100).
        """
        return self.progress

    def draw(self, screen: pygame.Surface):
        """Draw the progress bar on the screen.
        
        Renders the progress bar frame, background, and current progress.
        
        Args:
            screen: Pygame surface to draw on.
        """
        if self.icon:
            screen.blit(self.icon, (self.x, self.y))
        # Draw progress bar frame
        _h = self.size
        for i in range(2):
            _x = self.x_offset + self.x + i * self.size
            _y = self.y + 2 * self.size - i * self.size
            _w = self.width - i * self.size * 2 - self.x_offset
            pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
            pygame.draw.rect(screen, self.bg_color, (_x + self.size, _y, _w - self.size * 2, _h))
            _y = self.y + 3 * self.size + i * self.size
            pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
            pygame.draw.rect(screen, self.bg_color, (_x + self.size, _y, _w - self.size * 2, _h))

        _x = self.x + self.size * 2 + self.x_offset
        _y = self.y
        _w = self.width - self.size * 4 - self.x_offset
        pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
        _y = self.y + 5 * self.size
        pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))

        # Draw progress
        pygame.draw.rect(screen, self.border_color,
                         (self.bar_x + self.x_offset, self.bar_y, self.bar_w, self.bar_h))
