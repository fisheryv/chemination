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
    INTRO = "INTRO"
    MENU = "MENU"
    OPTIONS = "OPTIONS"
    CREDITS = "CREDITS"
    HELP = "HELP"
    BATTLE = "BATTLE"
    GAME_OVER = "GAME_OVER"


class Game:
    """游戏主类"""

    def __init__(self, screen):
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

        # 背景音乐
        load_background_music("bgm.mp3")
        # play_background_music()

    def main_menu(self):
        self.last_state = self.game_state
        self.game_state = SceneType.MENU
        self.current_scene = MainMenuScene(self)
        if self.last_state == SceneType.BATTLE or self.last_state == SceneType.GAME_OVER:
            load_background_music("bgm.mp3")

    def credits(self):
        self.last_state = self.game_state
        self.game_state = SceneType.CREDITS
        self.current_scene = CreditsScene(self)

    def options(self):
        self.last_state = self.game_state
        self.game_state = SceneType.OPTIONS
        self.current_scene = OptionsScene(self)

    def help(self):
        self.last_state = self.game_state
        self.game_state = SceneType.HELP
        self.current_scene = HelpScene(self)

    def battle(self):
        self.last_state = self.game_state
        self.game_state = SceneType.BATTLE
        self.current_scene = BattleScene(self)

    def music_toggle(self, state: bool):
        print(f"Music toggled: {state}")
        set_option("game", "music", "on" if state else "off")
        save_settings()
        if state:
            play_background_music()
        else:
            stop_background_music()

    def intro_toggle(self, state: bool):
        print(f"Intro toggled: {state}")
        set_option("game", "intro", "on" if state else "off")
        save_settings()

    def game_over(self):
        self.last_state = self.game_state
        self.game_state = SceneType.GAME_OVER
        self.current_scene = GameOverScene(self)

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        """游戏主循环"""
        while self.running:
            # 处理事件
            for event in pygame.event.get():
                self.current_scene.process_input(event)
                if event.type == pygame.QUIT:
                    self.running = False

            # 游戏逻辑更新
            self.current_scene.update()

            # 绘制
            self.current_scene.render(self.screen)
            pygame.display.flip()

            self.clock.tick(FPS)

        self.exit_game()
