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

    def __init__(self, x: float, y: float, dx: float, dy: float, size: float, color: pygame.Color):
        """Initialize a particle with the given parameters.
        
        Args:
            x:     Initial x position.
            y:     Initial y position.
            dx:    Velocity along x-axis.
            dy:    Velocity along y-axis.
            size:  Initial size of particle.
            color: RGB color tuple for the particle
        """
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.ds = self.size / 30.0
        self.color = color

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

    def draw(self, screen: pygame.Surface):
        """Draw the particle on screen.
        
        Args:
            screen: Pygame surface to draw on.
        """
        if self.is_alive():
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


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
            particle = Particle(x,
                                y,
                                random.uniform(-8, 8),
                                random.uniform(-8, 8),
                                random.randint(5, 10), color
                                )
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
            particle.draw(screen)


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


class FireParticle(Particle):
    """Represents a fire particle with specialized behavior and coloring."""

    def __init__(self, x: float, y: float, dx: float, dy: float, size: float, color: pygame.Color):
        """Initialize a fire particle with fire-like properties.
        
        Args:
            x:     Initial x position.
            y:     Initial y position.
            dx:    Velocity along x-axis.
            dy:    Velocity along y-axis (typically negative for rising fire).
            size:  Initial size of particle.
            color: RGB color tuple for the particle
        """
        super().__init__(x, y, dx, dy, size, color)
        self.life = 1.0  # Life percentage from 1.0 to 0.0
        self.initial_size = size

    def update(self):
        """Update fire particle position, size, and color."""
        if self.is_alive():
            # Apply gravity (particles rise and then fall)
            self.dy += 0.1

            # Apply friction
            self.dx *= 0.98
            self.dy *= 0.98

            # Update position
            self.x += self.dx
            self.y += self.dy

            # Decrease size over time
            self.size -= self.initial_size / 60.0

            # Update life percentage
            self.life = max(0.0, self.size / self.initial_size)

            # Change color as particle ages (from yellow-orange to dark red to black)
            # if self.life > 0.9:
            #     # Bright yellow-white core
            #     self.color = pygame.Color(255, 255, random.randint(100, 200))
            if self.life > 0.7:
                # Yellow-orange
                self.color = pygame.Color(255, int(100 + 100 * self.life), 0)
            elif self.life > 0.3:
                # Red-orange
                self.color = pygame.Color(int(255 * self.life), int(50 * self.life), 0)
            else:
                # Dark red to black
                intensity = int(100 * self.life)
                self.color = pygame.Color(intensity, 0, 0)

    def draw(self, screen: pygame.Surface):
        """Draw the fire particle on screen with its current color.
        
        Args:
            screen: Pygame surface to draw on.
        """
        if self.is_alive():
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


class FireEffect:
    """Represents a continuous fire effect composed of multiple fire particles."""

    def __init__(self, x: int, y: int, intensity: int = 5):
        """Initialize a continuous fire effect at the given position.
        
        Args:
            x:         X coordinate of fire effect center.
            y:         Y coordinate of fire effect center (base of fire).
            intensity: Number of particles to generate per update cycle.
        """
        self.x = x
        self.y = y
        self.intensity = intensity
        self.particles: list[FireParticle] = []
        self.timer = 0

    def update(self):
        """Update fire effect by adding new particles and updating existing ones."""
        self.timer += 1

        # Add new particles periodically
        if self.timer % 3 == 0:  # Add particles every 3 frames
            for _ in range(self.intensity):
                # Particles start at the base of the fire with some random offset for a wider base
                start_x = self.x + random.uniform(-15, 15)
                start_y = self.y + random.uniform(-3, 3)

                # Velocity: particles rise upward with more horizontal spread for a wider flame
                dx = random.uniform(-1.4, 1.4)
                dy = random.uniform(-10.0, -3.0)  # Negative for upward movement

                # Size: larger random initial size for better visibility
                size = random.uniform(3.0, 8.0)
                # Fire particles start with an intense orange-yellow color for increased brightness
                color = pygame.Color(255, random.randint(120, 220), random.randint(0, 20))
                particle = FireParticle(start_x, start_y, dx, dy, size, color)
                self.particles.append(particle)

        # Update existing particles
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen: pygame.Surface):
        """Draw the fire effect on screen.
        
        Args:
            screen: Pygame surface to draw on.
        """
        for particle in self.particles:
            particle.draw(screen)
