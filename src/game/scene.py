from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """Abstract base class for all game scenes.
    
    This class defines the common interface that all scenes must implement.
    Each scene represents a distinct state of the game, such as main menu, 
    gameplay, options screen, etc.
    """
    
    def __init__(self, parent):
        """Initialize the scene with a reference to the parent object.
        
        Args:
            parent: The parent object that contains this scene, typically 
                   the main game object.
        """
        self.parent = parent

    @abstractmethod
    def process_input(self, event: pygame.event.Event):
        """Process user input events for this scene.
        
        This method must be implemented by all subclasses to handle 
        user interactions like keyboard presses or mouse clicks.
        
        Args:
            event: The pygame event to process.
        """
        pass

    @abstractmethod
    def update(self):
        """Update the scene's state.
        
        This method must be implemented by all subclasses to update 
        the game logic, positions, animations, etc.
        """
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render the scene to the screen.
        
        This method must be implemented by all subclasses to draw 
        all visual elements of the scene to the screen.
        
        Args:
            screen: The pygame surface to render to.
        """
        pass