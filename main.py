"""Main entry point for the Chemination game.

This module serves as the main entry point for the Chemination game. It initializes
the pygame library, creates the game window, and starts the main game loop.
"""

import pygame
import sys

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, load_settings
from src.utils.tools import resource_path


def main():
    """Initialize and run the main game loop.
    
    This function initializes the pygame library, sets up the game window,
    loads settings, and starts the main game controller.
    """
    pygame.init()  # Initialize Pygame
    pygame.mixer.init()  # Initialize audio module

    try:
        # Set window icon
        icon = pygame.image.load(resource_path("icon.ico"))
        pygame.display.set_icon(icon)
    except Exception as e:
        print("Warning: Unable to load icon file icon.ico", e)

    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)

    # Load settings
    load_settings()

    # Import and run the main game class
    try:
        from src.game.game import Game
        game = Game(screen)
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
