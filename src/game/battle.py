import random

import pygame

from src.config.settings import PINK, WHITE, CYAN, SCREEN_WIDTH, BLACK, SCREEN_HEIGHT, GREEN, RED
from src.data.chemicals import ENEMIES
from src.entities.bullet import Bullet
from src.entities.button import ImageButton
from src.entities.enemy import Enemy
from src.entities.hero import Hero
from src.entities.processbar import ProcessBar
from src.game.scene import Scene
from src.utils.effects import EffectsManager
from src.utils.music import load_background_music, pause_background_music, resume_background_music
from src.utils.tools import resource_path


class BattleScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.is_running = True
        self.background = pygame.image.load(resource_path("assets/images/battle/battle_bg1.jpg"))  # 背景图
        self.rip = pygame.image.load(resource_path("assets/images/ui/rip.png"))
        self.rip = pygame.transform.scale(self.rip, (30, 30))
        self.pause_button = ImageButton(resource_path("assets/images/ui/pause.png"),
                                        SCREEN_WIDTH - 120, 10, 82, 30,
                                        action=self.pause_game)
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 20)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 24)

        self.hp = 100
        self.mp = 0

        self.hp_bar = ProcessBar(20, 10, 300, 30, PINK, WHITE, "hp.png")
        self.hp_bar.set_progress(self.hp)
        self.mp_bar = ProcessBar(360, 10, 300, 30, CYAN, WHITE, "mp.png")
        self.mp_bar.set_progress(self.mp)
        self.rectangle = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        self.rectangle.fill((255, 255, 255, 128))

        self.kill_count = 0
        self.kill_count_text = self.font.render("Kill Count:" + str(self.kill_count), True, BLACK)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group(self.pause_button)

        # 特效管理器
        self.effects_manager = EffectsManager()

        # 创建玩家
        self.player = Hero(self)
        self.all_sprites.add(self.player)

        # 暂停界面
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))
        self.pause_screen = pygame.image.load(resource_path("assets/images/ui/board.png"))
        self.start_button = ImageButton(resource_path("assets/images/ui/start.png"),
                                        (SCREEN_WIDTH - 127) / 2, SCREEN_HEIGHT/2-20, 127, 50,
                                        action=self.resume_game)
        self.stop_button = ImageButton(resource_path("assets/images/ui/stop.png"),
                                       (SCREEN_WIDTH - 127) / 2, SCREEN_HEIGHT/2+50, 127, 50,
                                       action=self.parent.main_menu)
        self.overlay_sprites = pygame.sprite.Group(self.start_button, self.stop_button)

        self.enemy_spawn_timer = 0

        # 加载背景音乐
        load_background_music("battle_bgm.mp3")
        # play_background_music()

    def pause_game(self):
        self.is_running = False
        pause_background_music()

    def resume_game(self):
        self.is_running = True
        resume_background_music()

    def spawn_enemy(self):
        """
        生成敌人
        """
        enemy_name = random.choice(list(ENEMIES.keys()))
        enemy = Enemy(enemy_name, ENEMIES[enemy_name])
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def shoot(self, x, y, direction, bullet_type):
        bullet = Bullet(x, y, direction, bullet_type)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self):
        if not self.is_running:
            return
        # 生成敌人
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 300:  # 每300帧生成一个敌人
            self.spawn_enemy()
            self.enemy_spawn_timer = 0

        # 更新精灵
        self.all_sprites.update()

        # 碰撞检测：子弹与敌人
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                is_killed = enemy.take_damage(bullet.bullet_type)
                if is_killed:
                    self.kill_count += 1
                    self.kill_count_text = self.font.render("Kill Count:" + str(self.kill_count), True, BLACK)
                    self.effects_manager.add_effect(enemy.rect.x, enemy.rect.centery, 'correct')

        # 更新特效
        self.effects_manager.update_effects()

    def render(self, screen):
        # 绘制背景
        screen.blit(self.background, (0, 0))
        # 绘制游戏数据
        screen.blit(self.rectangle, (0, 0))
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)
        screen.blit(self.rip, (700, 10))
        screen.blit(self.kill_count_text, (740, 12))
        # 绘制所有精灵
        self.ui_sprites.draw(screen)
        self.all_sprites.draw(screen)
        for e in self.enemies:
            e.draw_hp(screen)
        # 绘制特效
        self.effects_manager.draw_effects(screen, GREEN, RED)
        # 绘制暂停界面
        if not self.is_running:
            screen.blit(self.overlay, (0, 0))
            screen.blit(self.pause_screen, ((SCREEN_WIDTH - 504) / 2, (SCREEN_HEIGHT - 369) / 2))
            self.overlay_sprites.draw(screen)

    def process_input(self, event):
        if not self.is_running:
            self.overlay_sprites.update(event)
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()
        self.ui_sprites.update(event)
