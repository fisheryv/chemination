"""Visual effects system for the Chemination game.

This module contains classes and functions for creating visual effects
like particle systems for explosions, damage indicators, and other animations.
"""

import pygame
import random


class Particle:
    """Represents a single particle in a visual effect.
    
    This class handles particle physics, movement, and lifecycle management.
    """

    def __init__(self, x: float, y: float, dx: float, dy: float, size: float):
        """Initialize a particle with the given parameters.
        
        Args:
            x:    Initial x position.
            y:    Initial y position.
            dx:   Velocity along x-axis.
            dy:   Velocity along y-axis.
            size: Initial size of particle.
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.ds = self.size / 30.0

    def is_alive(self):
        """Check if particle is still alive (size > 0).
        
        Returns:
            bool: True if particle is still alive, False otherwise.
        """
        return self.size > 0

    def update(self):
        """Update particle position and size.
        
        Applies friction to velocity and decreases particle size over time.
        """
        if self.is_alive():
            self.dx *= 0.95
            self.dy *= 0.95
            self.x += self.dx
            self.y += self.dy
            self.size -= self.ds

    def draw(self, screen: pygame.Surface, color: pygame.Color):
        """Draw the particle on screen.
        
        Args:
            screen: Pygame surface to draw on.
            color:  RGB color tuple for the particle.
        """
        if self.is_alive():
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))


class Effect:
    """Represents a visual effect composed of multiple particles.
    
    This class manages a collection of particles that create a visual effect
    at a specific location, such as an explosion or damage indicator.
    """

    def __init__(self, x: int, y: int, color: pygame.Color):
        """Initialize an effect at the given position.
        
        Args:
            x:     X coordinate of effect.
            y:     Y coordinate of effect.
            color: RGB color tuple for the effect.
        """
        self.x = x
        self.y = y
        self.color = color
        self.timer = 30  # Effect duration in frames
        self.particles: list[Particle] = []

        # Create particles
        for i in range(10):
            particle = Particle(x, y, random.uniform(-8, 8), random.uniform(-8, 8), random.randint(5, 10))
            self.particles.append(particle)

    def is_alive(self):
        """Check if effect is still active.
        
        Returns:
            bool: True if effect is still active, False otherwise.
        """
        return self.timer > 0

    def update(self):
        """Update effect state and particles.
        
        Decrements the effect timer and updates all particles in the effect.
        """
        self.timer -= 1
        if self.timer > 0:
            # Update particle positions
            for particle in self.particles:
                particle.update()

    def draw(self, screen: pygame.Surface):
        """Draw the effect on screen.
        
        Args:
            screen: Pygame surface to draw on.
        """
        for particle in self.particles:
            particle.draw(screen, self.color)


class EffectsManager:
    """Manager for handling multiple visual effects.
    
    This class manages a collection of effects, handles their updates,
    and cleans up finished effects.
    """

    def __init__(self):
        """Initialize effects manager."""
        self.effects: list[Effect] = []  # Store effect instances

    def add_effect(self, x: int, y: int, color: pygame.Color):
        """Add a new effect to the manager.
        
        Args:
            x:     X coordinate of effect.
            y:     Y coordinate of effect.
            color: RGB color for the effect.
        """
        effect = Effect(x, y, color)
        self.effects.append(effect)

    def update_effects(self):
        """Update all active effects and remove expired ones.
        
        Updates each effect's state and removes effects that are no longer active.
        """
        for effect in self.effects:
            effect.timer -= 1
            if effect.is_alive():
                effect.update()
        self.effects = [effect for effect in self.effects if effect.is_alive()]

    def draw_effects(self, screen: pygame.Surface):
        """Draw all active effects on screen.
        
        Args:
            screen: Pygame surface to draw on.
        """
        for effect in self.effects:
            effect.draw(screen)
