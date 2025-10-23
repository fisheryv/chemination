"""Bullet entities for the Chemination game.

This module contains the Bullet class and BulletType enumeration that represent
the projectiles fired by the player's characters. Different bullet types correspond
to different hero types and have specific effects on enemies.
"""

from enum import Enum
import pygame

from src.config.settings import SCREEN_WIDTH
from src.utils.tools import load_sprite_row


class BulletType(Enum):
    """Enumeration of bullet types corresponding to hero types."""
    ACID = "acid"
    BASE = "base"
    METAL = "metal"


class Bullet(pygame.sprite.Sprite):
    """Represents a bullet projectile fired by the player.
    
    This class handles bullet movement, animation, and collision detection.
    """

    def __init__(self, x: int, y: int, direction: int, bullet_type: BulletType):
        """Initialize a bullet with the given parameters.
        
        Args:
            x:           Bullet initial x coordinate.
            y:           Bullet initial y coordinate.
            direction:   Bullet direction (-1: left, 1: right).
            bullet_type: Type of bullet to create.
        """
        super().__init__()
        self.bullet_type = bullet_type

        # Load bullet animation frames
        self.frames = load_sprite_row(
            f"assets/images/spirits/{self.bullet_type.value}.png",
            3,
            scale=1
        )

        # Animation related properties
        self.current_frame = 0
        self.animation_speed = 0.3
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Physical properties
        self.speed = 10
        self.direction = direction

        # Flip image based on direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        """Update the bullet's position and animation for each frame.
        
        Handles bullet movement, animation, and boundary checking. Removes the
        bullet when it flies off the screen.
        """
        # Update position
        self.rect.x += self.speed * self.direction

        # Update animation frames
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # Flip image based on direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Boundary check: remove bullet if it flies off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()