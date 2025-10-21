import random

import pygame

from src.config.settings import PINK, WHITE, CYAN, SCREEN_WIDTH, BLACK, SCREEN_HEIGHT, GREEN, RED, ENEMY_ESCAPED, \
    ENEMY_KILLED
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
        self.is_frozen = False
        self.background = pygame.image.load(resource_path("assets/images/battle/battle_bg1.jpg"))  # 背景图
        self.rip = pygame.image.load(resource_path("assets/images/ui/rip.png"))
        self.rip = pygame.transform.scale(self.rip, (30, 30))
        self.boom = pygame.image.load(resource_path("assets/images/ui/boom.png"))
        self.boom = pygame.transform.scale(self.boom, (30, 30))
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
        self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)

        self.boom_count = 3
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)

        # 粒子效果管理器
        self.effects_manager = EffectsManager()

        # 创建玩家
        self.player = Hero(self)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group(self.pause_button)

        # 特效管理器
        self.effects_manager = EffectsManager()

        # 暂停界面
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))
        self.pause_screen = pygame.image.load(resource_path("assets/images/ui/board.png"))
        self.start_button = ImageButton(resource_path("assets/images/ui/start.png"),
                                        (SCREEN_WIDTH - 127) / 2, SCREEN_HEIGHT / 2 - 20, 127, 50,
                                        action=self.resume_game)
        self.stop_button = ImageButton(resource_path("assets/images/ui/stop.png"),
                                       (SCREEN_WIDTH - 127) / 2, SCREEN_HEIGHT / 2 + 50, 127, 50,
                                       action=self.parent.main_menu)
        self.overlay_sprites = pygame.sprite.Group(self.start_button, self.stop_button)

        self.enemy_spawn_timer = 0
        self.frozen_timer = 0

        # 加载背景音乐
        load_background_music("battle_bgm.mp3")
        # play_background_music()

    def pause_game(self):
        """
        暂停游戏
        """
        self.is_running = False
        pause_background_music()

    def resume_game(self):
        """
        恢复游戏
        """
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
        self.enemy_spawn_timer = 0

    def freeze_enemy(self):
        self.is_frozen = True
        self.frozen_timer = 0
        self.boom_count -= 1
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)
        for e in self.enemies:
            e.freeze()

    def unfreeze_enemy(self):
        self.is_frozen = False
        self.frozen_timer = 0
        for e in self.enemies:
            e.unfreeze()

    def shoot(self, x, y, direction, bullet_type):
        """
        发射子弹
        """
        bullet = Bullet(x, y, direction, bullet_type)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self):
        if not self.is_running:  # 暂停状态停止更新
            return
        # 生成敌人
        if not self.is_frozen:
            self.enemy_spawn_timer += 1
            # 敌人生成速度随击杀数增加
            _interval = 300 - self.kill_count
            if _interval < 120:
                _interval = 120
            if self.enemy_spawn_timer >= _interval:
                self.spawn_enemy()
        else:
            self.frozen_timer += 1
            if self.frozen_timer >= 300:
                self.unfreeze_enemy()

        # 更新精灵
        self.all_sprites.update()

        # 检测玩家与敌人之间的碰撞
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for hit in hits:
            self.hp -= hit.health
            if self.hp <= 0:
                self.parent.game_over()
            self.hp_bar.set_progress(self.hp)
            self.effects_manager.add_effect(hit.rect.x, hit.rect.centery, 'wrong')
            # 删除敌人
            hit.kill()

        # 碰撞检测：子弹与敌人
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(bullet.bullet_type)

        # 更新特效
        self.effects_manager.update_effects()

    def render(self, screen):
        # 绘制背景
        screen.blit(self.background, (0, 0))
        # 绘制游戏数据
        screen.blit(self.rectangle, (0, 0))
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)
        _x = self.mp_bar.x + self.mp_bar.width + 10
        screen.blit(self.boom, (_x, 10))
        _x += self.boom.get_width()
        screen.blit(self.boom_count_text, (_x, 12))
        _x += 60
        screen.blit(self.rip, (_x, 10))
        _x += self.rip.get_width() + 10
        screen.blit(self.kill_count_text, (_x, 12))
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                _hero_type = self.player.hero_type
                _hero_type -= 1
                if _hero_type < 0:
                    _hero_type = 2
                self.player.change_hero(_hero_type)
            elif event.key == pygame.K_RIGHT:
                _hero_type = self.player.hero_type
                _hero_type += 1
                if _hero_type > 2:
                    _hero_type = 0
                self.player.change_hero(_hero_type)
            elif event.key == pygame.K_x:  # 释放技能
                if not self.is_frozen and self.boom_count > 0:
                    self.is_frozen = True
                    self.boom_count -= 1
                    self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)
                    for e in self.enemies:
                        e.freeze()
        elif event.type == pygame.MOUSEBUTTONUP:  # 敌人攻击
            if event.button == 1:  # 左键
                self.player.shoot()
            elif event.button == 3:  # 右键
                _hero_type = self.player.hero_type
                _hero_type += 1
                if _hero_type > 2:
                    _hero_type = 0
                self.player.change_hero(_hero_type)
        elif event.type == ENEMY_ESCAPED:  # 敌人逃逸
            enemy = event.dict.get('enemy', None)
            damage = event.dict.get('damage', 0)
            if enemy:
                self.hp -= damage
                self.hp_bar.set_progress(self.hp)
                self.effects_manager.add_effect(0, enemy.rect.centery, 'wrong')
                if self.hp <= 0:
                    self.parent.game_over()
        elif event.type == ENEMY_KILLED:  # 敌人击杀
            enemy = event.dict.get('enemy', None)
            if enemy:
                self.kill_count += 1
                self.mp += 10
                self.mp_bar.set_progress(self.mp)
                self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)
                self.effects_manager.add_effect(enemy.rect.x, enemy.rect.centery, 'correct')
                if self.kill_count % 10 == 0:
                    self.mp = 0
                    self.mp_bar.set_progress(self.mp)
                    self.boom_count += 1
                    self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)
        self.ui_sprites.update(event)
