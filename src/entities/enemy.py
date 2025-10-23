"""Enemy entities for the Chemination game.

This module contains the Enemy class that represents the chemical enemies
in the game. Each enemy has specific properties based on its chemical type
and behavior in the game world.
"""

import random
import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, ENEMY_ESCAPED, ENEMY_KILLED
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_row, resource_path


class Enemy(pygame.sprite.Sprite):
    """Represents a chemical enemy in the game.
    
    This class handles enemy behavior, including movement, animation,
    health management, and interactions with the player.
    """

    def __init__(self, name: str, params: dict):
        """Initialize an enemy with the given parameters.
        
        Args:
            name:   Enemy name (chemical formula).
            params: Enemy parameters (type, health, speed).
        """
        super().__init__()
        self.name = name
        self.params = params

        # Load enemy animation frames
        try:
            self.frames = load_sprite_row(f"assets/images/enemy/{name}.png", 4, scale=1)
        except pygame.error:
            # If unable to load image, create a default rectangle as substitute
            self.frames = [pygame.Surface((50, 50), pygame.SRCALPHA)]
            self.frames[0].fill((200, 100, 100, 200))

        # Load health icons
        try:
            self.heart1 = pygame.image.load(resource_path("assets/images/ui/heart1.png"))
            self.heart3 = pygame.image.load(resource_path("assets/images/ui/heart3.png"))
        except pygame.error:
            # If unable to load images, create simple substitute graphics
            self.heart1 = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.heart1.fill((255, 0, 0, 128))
            self.heart3 = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.heart3.fill((0, 255, 0, 128))

        # Animation related properties
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Position initialization (generated from random position on right side of screen)
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(120, SCREEN_HEIGHT - 120 - self.rect.height)

        # Physical properties
        self.speed = params["speed"]
        self.health = params["hp"]
        self.type = params["type"]

        # Render enemy name
        font = pygame.font.SysFont(None, 24)
        self.name_surface = font.render(self.name, True, WHITE)

        # Freeze state
        self.is_freeze = False

    def freeze(self):
        """Freeze the enemy, preventing movement.
        
        When frozen, the enemy will not move until unfrozen.
        """
        self.is_freeze = True

    def unfreeze(self):
        """Unfreeze the enemy, allowing movement again.
        
        Resumes normal enemy movement and behavior.
        """
        self.is_freeze = False

    def update(self):
        """Update the enemy's state for each frame.
        
        Handles enemy movement, animation, and boundary checking.
        If the enemy is frozen, no updates are performed.
        """
        # If frozen, do not update position
        if self.is_freeze:
            return

        # Update position
        self.rect.x -= self.speed

        # Update animation frames
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # Boundary check: if enemy leaves left side of screen, trigger escape event and delete
        if self.rect.right < 0:
            # Trigger enemy escape event
            pygame.event.post(pygame.event.Event(ENEMY_ESCAPED, {
                'enemy': self,
                'damage': self.health
            }))
            # Delete enemy
            self.kill()

    def draw_hp(self, screen: pygame.Surface):
        """Draw the enemy's health information on screen.
        
        Renders the enemy's health points as icons above the enemy sprite.
        
        Args:
            screen: Screen surface to draw on.
        """
        # Draw health icons
        _x = self.rect.x + (self.rect.width - self.heart1.get_width() * self.params["hp"]) / 2
        for i in range(self.params["hp"]):
            heart_image = self.heart3 if i < self.health else self.heart1
            screen.blit(heart_image, (_x + i * self.heart3.get_width(), self.rect.y - self.heart3.get_height()))

        # Draw enemy name
        _x = self.rect.x + (self.rect.width - self.name_surface.get_width()) / 2
        screen.blit(self.name_surface, (_x, self.rect.bottom))

    def take_damage(self, bullet_type: BulletType):
        """Apply damage to the enemy based on bullet type.
        
        Determines if the enemy is vulnerable to the bullet type and reduces
        health accordingly. If health reaches zero, the enemy is removed.
        
        Args:
            bullet_type: Type of bullet that hit the enemy.
        """
        # Determine if damage is taken
        if bullet_type == BulletType.ACID:
            _damage = self.type == "metal" or self.type == "base"
        elif bullet_type == BulletType.BASE:
            _damage = self.type == "acid"
        else:  # BulletType.METAL
            _damage = self.type == "salt"

        # If damage is taken, reduce health
        if _damage:
            self.health -= 1
            if self.health <= 0:
                # Trigger enemy kill event
                pygame.event.post(pygame.event.Event(ENEMY_KILLED, {
                    'enemy': self,
                    'damage': 0
                }))
                # Delete enemy
                self.kill()