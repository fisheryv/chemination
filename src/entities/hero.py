"""Player character entities for the Chemination game.

This module contains the Hero and Avatar classes that represent the player's characters
in the game. It handles character animations, movement, shooting, and switching between
different hero types (Base Knight, Acid Hitman, and Metal Elf).
"""

import pygame
from pygame.locals import *

from src.config.settings import SCREEN_HEIGHT, HERO_ATTACK
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_sheet, load_sprite_row

# Bullet type mapping
BULLET_TYPES = [BulletType.BASE, BulletType.ACID, BulletType.METAL]


class Avatar:
    """Represents the visual appearance of a player character.
    
    This class handles the loading and management of character animations,
    including walking and attack animations for different hero types.
    """

    def __init__(self, hero_type: int):
        """Initialize character appearance.
        
        Args:
            hero_type: Character type (0: base, 1: acid, 2: metal)
        """
        self.hero_type = hero_type

        # Load walking animation frames (down, left, up directions)
        try:
            self.animations = load_sprite_sheet(
                f"assets/images/spirits/hero{self.hero_type + 1}.png",
                3, 4,
                directions=("down", "left", "up"),
                scale=1
            )
        except pygame.error:
            # If unable to load image, create simple substitute graphics
            self.animations = self._create_default_animations()

        # Generate right walking frames through horizontal mirroring
        direction_frames = []
        for f in self.animations["left"]:
            direction_frames.append(pygame.transform.flip(f, True, False))
        self.animations["right"] = direction_frames

        # Load attack animation
        try:
            self.attack = load_sprite_row(
                f"assets/images/spirits/hero{self.hero_type + 1}_attack.png",
                4,
                scale=1
            )
        except pygame.error:
            # If unable to load attack animation, use the first frame of walking animation as substitute
            self.attack = self.animations["right"][:4] if len(self.animations["right"]) >= 4 else [self.animations[
                                                                                                       "right"][0]] * 4

    def _create_default_animations(self):
        """Create default animation frames for fallback graphics.
        
        Creates simple colored rectangles as substitute graphics when image files
        cannot be loaded. Each character type gets a different color.
        
        Returns:
            dict: Dictionary mapping directions to lists of animation frames.
        """
        # Create a simple colored rectangle as default character appearance
        default_frames = []
        colors = [pygame.Color(100, 100, 255, 200),  # BLUE
                  pygame.Color(100, 255, 100, 200),  # GREEN
                  pygame.Color(255, 100, 100, 200),  # RED
                  ]
        for color in colors:
            frame = pygame.Surface((50, 80), pygame.SRCALPHA)
            frame.fill(color)  # Fill color
            default_frames.append(frame)

        # Assign frames to different directions
        return {
            "down": [default_frames[0]],
            "left": [default_frames[1]],
            "up": [default_frames[2]],
            "right": [default_frames[1]]  # Right direction uses mirrored left direction
        }


class Hero(pygame.sprite.Sprite):
    """Main player character class.
    
    This class represents the player-controlled character in the game. It handles
    character movement, animation, shooting, and switching between different hero types.
    """

    def __init__(self):
        """Initialize player character.
        
        Sets up the initial state of the player character, including position,
        animation properties, and physical attributes.
        """
        super().__init__()
        self.hero_type = 0  # Default character type (base)

        # Create character appearance instances
        self.avatars = [Avatar(0), Avatar(1), Avatar(2)]

        # Animation related properties
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        # Physical properties
        self.speed = 5
        self.last_shot = 0
        self.shoot_delay = 300  # milliseconds

        # Status properties
        self.walking = False
        self.direction = 1  # 1 right, -1 left
        self.attacking = False

    def change_hero(self, hero_type: int):
        """Switch to a different character type.
        
        Changes the current hero type and updates the character's visual appearance
        while maintaining the character's position on screen.
        
        Args:
            hero_type: New character type (0: base, 1: acid, 2: metal)
        """
        self.hero_type = hero_type
        old_center = self.rect.center
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        """Update the character's state for each frame.
        
        Handles character animations, movement, and input processing. This method
        is called once per frame to update the character's position and appearance.
        """
        # Handle attack animation
        if self.attacking:
            self.current_frame += 0.25
            if self.current_frame >= len(self.avatars[self.hero_type].attack):
                self.current_frame = 0
                self.attacking = False
                # Trigger attack event
                pygame.event.post(pygame.event.Event(HERO_ATTACK, {
                    'x': self.rect.centerx,
                    'y': self.rect.centery,
                    'direction': self.direction,
                    'bullet_type': BULLET_TYPES[self.hero_type]
                }))
            self.image = self.avatars[self.hero_type].attack[int(self.current_frame)]
            return

        # Get key state
        keys = pygame.key.get_pressed()

        # Switch character type
        if keys[K_1]:
            self.change_hero(0)  # Base
        elif keys[K_2]:
            self.change_hero(1)  # Acid
        elif keys[K_3]:
            self.change_hero(2)  # Salt

        # Handle movement
        self.walking = False

        # Horizontal movement (commented out, can be uncommented if needed)
        # if keys[K_LEFT] or keys[K_a]:
        #     self.current_direction = 'left'
        #     self.rect.x -= self.speed
        #     self.walking = True
        #     self.direction = -1
        # if keys[K_RIGHT] or keys[K_d]:
        #     self.current_direction = 'right'
        #     self.rect.x += self.speed
        #     self.walking = True
        #     self.direction = 1

        # Vertical movement
        if keys[K_UP] or keys[K_w]:
            self.current_direction = 'up'
            self.rect.y -= self.speed
            self.walking = True
        if keys[K_DOWN] or keys[K_s]:
            self.current_direction = 'down'
            self.rect.y += self.speed
            self.walking = True

        # Boundary check
        # Limit horizontal movement boundary (can be uncommented if needed)
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH

        # Limit vertical movement boundary
        if self.rect.top < 120:
            self.rect.top = 120
        if self.rect.bottom > SCREEN_HEIGHT - 120:
            self.rect.bottom = SCREEN_HEIGHT - 120

        # Update animation frames
        if self.walking:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.avatars[self.hero_type].animations[self.current_direction]):
                self.current_frame = 0
            self.image = self.avatars[self.hero_type].animations[self.current_direction][int(self.current_frame)]
        else:
            # Use first frame when idle
            self.image = self.avatars[self.hero_type].animations[self.current_direction][0]

    def shoot(self):
        """Fire a bullet from the character's current position.
        
        Creates a bullet projectile based on the current hero type and direction.
        Implements a delay between shots to prevent continuous firing.
        """
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.attacking = True
            self.current_frame = 0
            self.current_direction = "right"
