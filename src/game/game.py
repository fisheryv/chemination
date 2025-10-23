"""Main game controller and scene manager.

This module contains the main Game class that serves as the central controller
for the Chemination game. It manages game state, scene transitions, and the
main game loop.
"""

from enum import Enum

import sys
from src.config.settings import *
from src.game.battle import BattleScene
from src.game.credits import CreditsScene
from src.game.game_over import GameOverScene
from src.game.help import HelpScene
from src.game.options import OptionsScene
from src.game.story import StoryScene
from src.game.main_menu import MainMenuScene
from src.utils.music import play_background_music, stop_background_music, load_background_music


class SceneType(Enum):
    """Enumeration of all possible game scenes."""
    INTRO = "INTRO"
    MENU = "MENU"
    OPTIONS = "OPTIONS"
    CREDITS = "CREDITS"
    HELP = "HELP"
    BATTLE = "BATTLE"
    GAME_OVER = "GAME_OVER"


class Game:
    """Main game controller class.
    
    This class manages the game's main loop, scene transitions, and overall game state.
    It serves as the central coordinator between different game components.
    """

    def __init__(self, screen: pygame.Surface):
        """Initialize the game and set up the initial state.
        
        Args:
            screen: The pygame surface to render the game on.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_state = None
        _intro = get_option("game", "intro")
        if _intro == "on":
            self.game_state = SceneType.INTRO
            self.current_scene = StoryScene(self)
        else:
            self.game_state = SceneType.MENU
            self.current_scene = MainMenuScene(self)

        # Background music
        load_background_music("bgm.mp3")
        # play_background_music()

    def main_menu(self):
        """Switch to the main menu scene.
        
        Transitions the game to the main menu scene and loads the appropriate
        background music for the menu.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.MENU
        self.current_scene = MainMenuScene(self)
        if self.last_state == SceneType.BATTLE or self.last_state == SceneType.GAME_OVER:
            load_background_music("bgm.mp3")

    def credits(self):
        """Switch to the credits scene.
        
        Transitions the game to the credits scene to display game credits and information.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.CREDITS
        self.current_scene = CreditsScene(self)

    def options(self):
        """Switch to the options scene.
        
        Transitions the game to the options scene where players can adjust game settings.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.OPTIONS
        self.current_scene = OptionsScene(self)

    def help(self):
        """Switch to the help scene.
        
        Transitions the game to the help scene where players can view game instructions
        and information about game mechanics.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.HELP
        self.current_scene = HelpScene(self)

    def battle(self):
        """Switch to the battle scene.
        
        Transitions the game to the main battle scene where gameplay occurs.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.BATTLE
        self.current_scene = BattleScene(self)

    def music_toggle(self, state: bool):
        """Toggle background music on or off.
        
        Args:
            state: True to enable music, False to disable music.
        """
        set_option("game", "music", "on" if state else "off")
        save_settings()
        if state:
            play_background_music()
        else:
            stop_background_music()

    def intro_toggle(self, state: bool):
        """Toggle whether to show the intro scene.
        
        Args:
            state: True to show intro, False to skip intro.
        """
        set_option("game", "intro", "on" if state else "off")
        save_settings()

    def game_over(self):
        """Switch to the game over scene.
        
        Transitions the game to the game over scene when the player's health reaches zero.
        """
        self.last_state = self.game_state
        self.game_state = SceneType.GAME_OVER
        self.current_scene = GameOverScene(self)

    def exit_game(self):
        """Exit the game and close the application.
        
        Properly shuts down the pygame library and exits the application.
        """
        pygame.quit()
        sys.exit()

    def run(self):
        """Run the main game loop.
        
        This is the core game loop that handles events, updates game state,
        renders graphics, and maintains the frame rate. The loop continues
        until the game is exited.
        """
        while self.running:
            # Handle events
            for event in pygame.event.get():
                self.current_scene.process_input(event)
                if event.type == pygame.QUIT:
                    self.running = False

            # Update game logic
            self.current_scene.update()

            # Render
            self.current_scene.render(self.screen)
            pygame.display.flip()

            # Clock tick
            self.clock.tick(FPS)

        self.exit_game()