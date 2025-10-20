from enum import Enum

import pygame
import random
import time
import sys
from src.config.settings import *
from src.data.chemicals import get_formulas_by_difficulty
from src.entities.block import ChemicalBlock
from src.entities.player import Player
from src.game.battle import BattleScene
from src.game.credits import CreditsScene
from src.game.game_over import GameOverScene
from src.game.options import OptionsScene
from src.game.story import StoryScene
from src.utils.effects import EffectsManager
from src.utils.hud import HUD
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
        _intro = get_option("game", "intro")
        if _intro == "on":
            self.game_state = SceneType.INTRO
            self.current_scene = StoryScene(self)
        else:
            self.game_state = SceneType.MENU
            self.current_scene = MainMenuScene(self)
        self.last_state = None
        self.player = None
        self.blocks = []
        self.start_time = 0
        self.game_time = 0
        self.last_hp_decrease = 0
        self.last_block_spawn = 0
        self.score = 0

        # 特效管理器
        self.effects_manager = EffectsManager()

        # HUD
        self.hud = HUD()

        # 背景音乐
        load_background_music("bgm.mp3")
        # play_background_music()

    def main_menu(self):
        self.last_state = self.game_state
        self.game_state = SceneType.MENU
        self.current_scene = MainMenuScene(self)
        if self.last_state == SceneType.BATTLE:
            load_background_music("bgm.mp3")

    def credits(self):
        self.last_state = self.game_state
        self.game_state = SceneType.CREDITS
        self.current_scene = CreditsScene(self)

    def options(self):
        self.last_state = self.game_state
        self.game_state = SceneType.OPTIONS
        self.current_scene = OptionsScene(self)

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

    def get_current_difficulty(self):
        """获取当前难度等级"""
        if self.game_time > 60:
            return "HARD"
        elif self.game_time > 30:
            return "MEDIUM"
        else:
            return "EASY"

    def run(self):
        """游戏主循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # 处理事件
            for event in pygame.event.get():
                self.current_scene.process_input(event)
                if event.type == pygame.QUIT:
                    self.running = False

            # 游戏逻辑更新
            self.current_scene.update()
            if self.game_state == "PLAYING":
                # 更新游戏时间
                self.game_time = time.time() - self.start_time

                # 处理键盘输入
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.player.move_left()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.player.move_right()

                # 每秒扣减2HP
                current_time = time.time()
                if current_time - self.last_hp_decrease >= 1:
                    self.player.take_damage(3)
                    self.last_hp_decrease = current_time

                # 生成新方块
                spawn_interval = max(0.8, 2 - self.game_time / 60)  # 随时间增加生成频率
                if current_time - self.last_block_spawn >= spawn_interval:
                    self.spawn_block()
                    self.last_block_spawn = current_time

                # 更新方块
                for block in self.blocks[:]:
                    block.update()

                    # 检查碰撞
                    if self.check_collision(self.player, block):
                        # 判断是否是正确的类型
                        if block.type == self.player.role:
                            self.player.heal(5)
                            self.score += 10
                            self.effects_manager.add_effect(block.rect.centerx, block.rect.centery, 'correct')
                        else:
                            self.player.take_damage(30)
                            self.effects_manager.add_effect(block.rect.centerx, block.rect.centery, 'wrong')

                        self.blocks.remove(block)

                    # 检查是否掉出屏幕
                    elif block.is_off_screen():
                        # 如果是应该接住的类型但没接住
                        if block.type == self.player.role:
                            self.player.take_damage(20)
                        self.blocks.remove(block)

                # 更新特效
                self.effects_manager.update_effects()

                # 检查游戏结束
                if self.player.hp <= 0:
                    self.game_state = "GAME_OVER"

            # 绘制
            self.current_scene.render(self.screen)
            pygame.display.flip()

        self.exit_game()
