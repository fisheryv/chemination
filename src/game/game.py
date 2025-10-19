import pygame
import random
import time
import sys
from src.config.settings import *
from src.data.chemicals import get_formulas_by_difficulty
from src.entities.block import ChemicalBlock
from src.entities.player import Player
from src.game.credits import CreditsScene
from src.game.game_over import GameOverScene
from src.game.options import OptionsScene
from src.utils.effects import EffectsManager
from src.utils.hud import HUD
from src.game.main_menu import MainMenuScene
from src.utils.tools import resource_path


class Game:
    """游戏主类"""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("simhei.ttf", 20) if pygame.font.match_font("simhei.ttf") else pygame.font.Font(
            None, 20)
        self.big_font = pygame.font.Font("simhei.ttf", 36) if pygame.font.match_font(
            "simhei.ttf") else pygame.font.Font(None, 36)
        self.block_font = pygame.font.Font("simhei.ttf", 28) if pygame.font.match_font(
            "simhei.ttf") else pygame.font.Font(None, 28)

        self.running = True
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.current_scene = MainMenuScene(self)
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
        self.bg_music = None
        self.music_loaded = False
        self.music_playing = False
        self.load_background_music()

    def main_menu(self):
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.current_scene = MainMenuScene(self)

    def credits(self):
        self.game_state = "CREDITS"  # MENU, PLAYING, GAME_OVER
        self.current_scene = CreditsScene(self)

    def options(self):
        self.game_state = "OPTIONS"  # MENU, PLAYING, GAME_OVER
        self.current_scene = OptionsScene(self)

    def music_toggle(self, state: bool):
        print(f"Music toggled: {state}")
        set_option("game", "music", "on" if state else "off")
        save_settings()
        if state:
            self.play_background_music()
        else:
            self.stop_background_music()

    def intro_toggle(self, state: bool):
        print(f"Intro toggled: {state}")
        set_option("game", "intro", "on" if state else "off")
        save_settings()

    def game_over(self):
        self.game_state = "GAME_OVER"  # MENU, PLAYING, GAME_OVER
        self.current_scene = GameOverScene(self)

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def load_background_music(self):
        """加载背景音乐"""
        try:
            music_path = os.path.join("assets/audios", "bgm.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(resource_path(music_path))
                pygame.mixer.music.set_volume(0.7)  # 设置音量
                self.music_loaded = True
                print("Background music loaded successfully")
                if get_option("game", "music") == "off":
                    self.stop_background_music()
                else:
                    self.play_background_music()
            else:
                print(f"Background music file not found: {music_path}")
        except pygame.error as e:
            print(f"Failed to load background music: {e}")
        except Exception as e:
            print(f"Unexpected error while loading background music: {e}")

    def play_background_music(self):
        """播放背景音乐"""
        if self.music_loaded:
            pygame.mixer.music.play(-1)  # -1 表示循环播放
            self.music_playing = True

    def stop_background_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_background_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()
        self.music_playing = False

    def unpause_background_music(self):
        """恢复背景音乐"""
        pygame.mixer.music.unpause()
        self.music_playing = True

    def show_menu(self):
        """显示主菜单"""
        self.screen.fill(WHITE)

        # 标题
        title = self.big_font.render("ACID BASE SALT BLOCK RAIN", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        subtitle = self.font.render("CHOOSE YOUR ROLE", True, DARK_GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)

        # 角色选择按钮
        buttons = []

        # 酸按钮
        acid_btn = pygame.Rect(SCREEN_WIDTH // 2 - 250, 250, 150, 80)
        pygame.draw.rect(self.screen, RED, acid_btn)
        pygame.draw.rect(self.screen, DARK_RED, acid_btn, 3)
        acid_text = self.big_font.render("ACID", True, BLACK)
        acid_text_rect = acid_text.get_rect(center=acid_btn.center)
        self.screen.blit(acid_text, acid_text_rect)
        buttons.append(('acid', acid_btn))

        # 碱按钮
        base_btn = pygame.Rect(SCREEN_WIDTH // 2 - 75, 250, 150, 80)
        pygame.draw.rect(self.screen, BLUE, base_btn)
        pygame.draw.rect(self.screen, DARK_BLUE, base_btn, 3)
        base_text = self.big_font.render("BASE", True, BLACK)
        base_text_rect = base_text.get_rect(center=base_btn.center)
        self.screen.blit(base_text, base_text_rect)
        buttons.append(('base', base_btn))

        # 盐按钮
        salt_btn = pygame.Rect(SCREEN_WIDTH // 2 + 100, 250, 150, 80)
        pygame.draw.rect(self.screen, GREEN, salt_btn)
        pygame.draw.rect(self.screen, DARK_GREEN, salt_btn, 3)
        salt_text = self.big_font.render("SALT", True, BLACK)
        salt_text_rect = salt_text.get_rect(center=salt_btn.center)
        self.screen.blit(salt_text, salt_text_rect)
        buttons.append(('salt', salt_btn))

        # 游戏说明
        instructions = [
            "Game Instructions: ",
            "1. After selecting a character, catch the corresponding type of chemical formula. ",
            "2. Initial HP = 500, correct catch +5 HP, wrong catch -30 HP, missed catch -20 HP. ",
            "3. Lose 3 HP per second automatically; the game ends when HP reaches zero. ",
            "4. Use the arrow keys to move."
        ]

        y_offset = 380
        for instruction in instructions:
            text = self.font.render(instruction, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        # 音乐控制提示
        if self.music_loaded:
            music_status = "ON" if self.music_playing else "OFF"
            music_text = self.font.render(f"Music: {music_status} (Press 'M' to toggle)", True, DARK_GRAY)
            music_rect = music_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 30))
            self.screen.blit(music_text, music_rect)

        return buttons

    def show_game_over(self):
        """显示游戏结束画面"""
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        # 显示成绩
        time_text = self.font.render(f"SIRVIVAL TIME: {self.game_time:.1f} s", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(time_text, time_rect)

        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(score_text, score_rect)

        # 重新开始提示
        restart_text = self.font.render("Press SPACE to return to the main menu", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)

    def spawn_block(self):
        """生成新的化学式方块"""

        # 根据游戏时间调整难度
        if self.game_time > 60:
            difficulty = 'hard'
        elif self.game_time > 30:
            difficulty = 'medium'
        else:
            difficulty = 'easy'

        # 随机选择化学式类型
        block_type = random.choice(['acid', 'base', 'salt'])

        # 根据类型选择化学式
        if block_type == 'acid':
            formula = random.choice(get_formulas_by_difficulty(difficulty)['acids'])
        elif block_type == 'base':
            formula = random.choice(get_formulas_by_difficulty(difficulty)['bases'])
        else:
            formula = random.choice(get_formulas_by_difficulty(difficulty)['salts'])

        # 随机x位置
        x = random.randint(50, SCREEN_WIDTH - 150)

        # 创建方块
        block = ChemicalBlock(formula, block_type, x, -60)

        # 根据游戏时间调整速度
        if self.game_time > 60:
            block.speed = 6
        elif self.game_time > 30:
            block.speed = 4

        self.blocks.append(block)

    def check_collision(self, player, block):
        """检查玩家与方块的碰撞"""
        return player.rect.colliderect(block.rect)

    def reset_game(self):
        """重置游戏"""
        self.blocks = []
        self.start_time = time.time()
        self.game_time = 0
        self.last_hp_decrease = time.time()
        self.last_block_spawn = time.time()
        self.score = 0
        self.effects_manager = EffectsManager()  # Reset effects manager

        # 开始播放背景音乐
        if self.music_loaded and not self.music_playing:
            self.play_background_music()

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

                if self.game_state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        buttons = self.show_menu()
                        for role, rect in buttons:
                            if rect.collidepoint(mouse_pos):
                                self.player = Player(role)
                                self.reset_game()
                                self.game_state = "PLAYING"
                    elif event.type == pygame.KEYDOWN:
                        # 音乐控制
                        if event.key == pygame.K_m:
                            if self.music_loaded:
                                if self.music_playing:
                                    self.pause_background_music()
                                else:
                                    if self.music_loaded:
                                        self.unpause_background_music() if hasattr(self,
                                                                                   'music_loaded') and self.music_loaded else self.play_background_music()

                elif self.game_state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_state = "MENU"
                        # 音乐控制
                        elif event.key == pygame.K_m:
                            if self.music_loaded:
                                if self.music_playing:
                                    self.pause_background_music()
                                else:
                                    self.unpause_background_music()

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

                # 音乐控制
                if keys[pygame.K_m]:
                    if self.music_loaded:
                        if self.music_playing:
                            self.pause_background_music()
                        else:
                            self.unpause_background_music()
                        # 添加一个小延迟以防止重复触发
                        pygame.time.delay(200)

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
                    # 停止背景音乐
                    if self.music_playing:
                        self.stop_background_music()

            # 绘制
            self.screen.fill(WHITE)
            self.current_scene.render(self.screen)
            # print(f"Drawing frame, game_state: {self.game_state}")  # Debug output

            # if self.game_state == "MENU":
            #     self.show_menu()
            #
            # elif self.game_state == "PLAYING":
            #     # 绘制游戏元素
            #     self.player.draw(self.screen, self.font)
            #
            #     for block in self.blocks:
            #         block.draw(self.screen, self.block_font)
            #
            #     # 绘制特效
            #     self.effects_manager.draw_effects(self.screen, GREEN, RED)
            #
            #     # 绘制HUD
            #     current_difficulty = self.get_current_difficulty()
            #     self.hud.draw_hud(self.screen, self.font, self.player, self.game_time, self.score, current_difficulty)
            #
            # elif self.game_state == "GAME_OVER":
            #     # 先绘制游戏画面
            #     self.player.draw(self.screen, self.font)
            #     for block in self.blocks:
            #         block.draw(self.screen, self.block_font)
            #     current_difficulty = self.get_current_difficulty()
            #     self.hud.draw_hud(self.screen, self.font, self.player, self.game_time, self.score, current_difficulty)
            #
            #     # 然后绘制游戏结束画面
            #     self.show_game_over()

            pygame.display.flip()

        self.exit_game()
