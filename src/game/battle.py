import random
import pygame

from src.config.settings import (
    PINK, WHITE, CYAN, SCREEN_WIDTH, BLACK, SCREEN_HEIGHT,
    ENEMY_ESCAPED, ENEMY_KILLED, HERO_ATTACK, RED,  GREEN
)
from src.data.chemicals import ENEMIES
from src.entities.bullet import Bullet, BulletType
from src.entities.button import ImageButton
from src.entities.enemy import Enemy
from src.entities.hero import Hero
from src.entities.processbar import ProcessBar
from src.game.scene import Scene
from src.utils.effects import EffectsManager
from src.utils.music import (
    load_background_music, pause_background_music, resume_background_music
)
from src.utils.tools import resource_path


class BattleScene(Scene):
    """战斗场景类"""

    def __init__(self, parent):
        """
        初始化战斗场景
        
        Args:
            parent (Game): 游戏主类实例
        """
        super().__init__(parent)

        # 游戏状态
        self.is_running = True
        self.is_frozen = False

        # 加载资源
        self._load_resources()

        # 初始化游戏数据
        self._init_game_data()

        # 创建玩家和精灵组
        self._init_sprites()

        # 初始化特效管理器
        self.effects_manager = EffectsManager()

        # 初始化暂停界面
        self._init_pause_screen()

        # 计时器
        self.enemy_spawn_timer = 0
        self.frozen_timer = 0

        # 加载背景音乐
        load_background_music("battle_bgm.mp3")

    def _load_resources(self):
        """加载游戏资源"""
        try:
            self.background = pygame.image.load(resource_path("assets/images/battle/battle_bg1.jpg"))
        except pygame.error:
            # 如果无法加载背景图，创建一个纯色背景作为替代
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 100))

        try:
            self.rip = pygame.image.load(resource_path("assets/images/ui/rip.png"))
            self.rip = pygame.transform.scale(self.rip, (30, 30))
        except pygame.error:
            # 创建简单的替代图形
            self.rip = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.rip.fill((255, 0, 0, 128))

        try:
            self.boom = pygame.image.load(resource_path("assets/images/ui/boom.png"))
            self.boom = pygame.transform.scale(self.boom, (30, 30))
        except pygame.error:
            # 创建简单的替代图形
            self.boom = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.boom.fill((255, 255, 0, 128))

        # 暂停按钮
        self.pause_button = ImageButton(
            resource_path("assets/images/ui/pause.png"),
            SCREEN_WIDTH - 120, 10, 82, 30,
            action=self.pause_game
        )

        # 加载字体
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 20)
        except (FileNotFoundError, pygame.error):
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 24)

    def _init_game_data(self):
        """初始化游戏数据"""
        # 玩家属性
        self.hp = 100
        self.mp = 0

        # 进度条
        self.hp_bar = ProcessBar(20, 10, 300, 30, PINK, WHITE, "hp.png")
        self.hp_bar.set_progress(self.hp)
        self.mp_bar = ProcessBar(360, 10, 300, 30, CYAN, WHITE, "mp.png")
        self.mp_bar.set_progress(self.mp)

        # 顶部信息栏
        self.rectangle = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        self.rectangle.fill((255, 255, 255, 128))

        # 击杀计数
        self.kill_count = 0
        self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)

        # 技能点数
        self.boom_count = 3
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)

    def _init_sprites(self):
        """初始化精灵组"""
        # 创建玩家
        self.player = Hero()

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group(self.pause_button)

    def _init_pause_screen(self):
        """初始化暂停界面"""
        # 暂停遮罩
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))

        # 暂停面板
        try:
            self.pause_screen = pygame.image.load(resource_path("assets/images/ui/board.png"))
        except pygame.error:
            # 创建简单的替代图形
            self.pause_screen = pygame.Surface((504, 369), pygame.SRCALPHA)
            self.pause_screen.fill((100, 100, 100, 200))

        # 暂停界面按钮
        self.start_button = ImageButton(
            resource_path("assets/images/ui/start.png"),
            (SCREEN_WIDTH - 127) // 2, SCREEN_HEIGHT // 2 - 20, 127, 50,
            action=self.resume_game
        )
        self.stop_button = ImageButton(
            resource_path("assets/images/ui/stop.png"),
            (SCREEN_WIDTH - 127) // 2, SCREEN_HEIGHT // 2 + 50, 127, 50,
            action=self.parent.main_menu
        )
        self.overlay_sprites = pygame.sprite.Group(self.start_button, self.stop_button)

    def pause_game(self):
        """暂停游戏"""
        self.is_running = False
        pause_background_music()

    def resume_game(self):
        """恢复游戏"""
        self.is_running = True
        resume_background_music()

    def spawn_enemy(self):
        """生成敌人"""
        enemy_name = random.choice(list(ENEMIES.keys()))
        enemy = Enemy(enemy_name, ENEMIES[enemy_name])
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)
        self.enemy_spawn_timer = 0

    def freeze_enemy(self):
        """冻结所有敌人"""
        self.is_frozen = True
        self.frozen_timer = 0
        self.boom_count -= 1
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)
        for e in self.enemies:
            e.freeze()

    def unfreeze_enemy(self):
        """解冻所有敌人"""
        self.is_frozen = False
        self.frozen_timer = 0
        for e in self.enemies:
            e.unfreeze()

    def shoot(self, x: int, y: int, direction: int, bullet_type: BulletType):
        """
        发射子弹
        
        Args:
            x (int): 子弹初始x坐标
            y (int): 子弹初始y坐标
            direction (int): 子弹方向
            bullet_type (BulletType): 子弹类型
        """
        bullet = Bullet(x, y, direction, bullet_type)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self):
        """更新游戏状态"""
        # 暂停状态不更新
        if not self.is_running:
            return

        # 生成敌人
        if not self.is_frozen:
            self.enemy_spawn_timer += 1
            # 敌人生成速度随击杀数增加（最少间隔120帧）
            spawn_interval = max(300 - self.kill_count, 120)
            if self.enemy_spawn_timer >= spawn_interval:
                self.spawn_enemy()
        else:
            # 更新冻结计时器
            self.frozen_timer += 1
            if self.frozen_timer >= 300:  # 冻结300帧后解冻
                self.unfreeze_enemy()

        # 更新所有精灵
        self.all_sprites.update()

        # 检测玩家与敌人之间的碰撞
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for hit in hits:
            self.hp -= hit.health
            if self.hp <= 0:
                self.parent.game_over()
            self.hp_bar.set_progress(self.hp)
            self.effects_manager.add_effect(hit.rect.x, hit.rect.centery, RED)
            # 删除敌人
            hit.kill()

        # 碰撞检测：子弹与敌人
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(bullet.bullet_type)

        # 更新特效
        self.effects_manager.update_effects()

    def render(self, screen: pygame.Surface):
        """
        渲染游戏画面
        
        Args:
            screen (pygame.Surface): 屏幕表面
        """
        # 绘制背景
        screen.blit(self.background, (0, 0))

        # 绘制游戏数据栏
        screen.blit(self.rectangle, (0, 0))
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)

        # 绘制技能图标和数量
        x_pos = self.mp_bar.x + self.mp_bar.width + 10
        screen.blit(self.boom, (x_pos, 10))
        x_pos += self.boom.get_width()
        screen.blit(self.boom_count_text, (x_pos, 12))

        # 绘制击杀计数
        x_pos += 60
        screen.blit(self.rip, (x_pos, 10))
        x_pos += self.rip.get_width() + 10
        screen.blit(self.kill_count_text, (x_pos, 12))

        # 绘制所有精灵
        self.ui_sprites.draw(screen)
        self.all_sprites.draw(screen)
        for e in self.enemies:
            e.draw_hp(screen)

        # 绘制特效
        self.effects_manager.draw_effects(screen)

        # 绘制暂停界面
        if not self.is_running:
            screen.blit(self.overlay, (0, 0))
            screen.blit(self.pause_screen, ((SCREEN_WIDTH - 504) / 2, (SCREEN_HEIGHT - 369) / 2))
            self.overlay_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """
        处理输入事件
        
        Args:
            event (pygame.event.Event): pygame事件
        """
        # 处理暂停界面事件
        if not self.is_running:
            self.overlay_sprites.update(event)
            return

        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()

        elif event.type == pygame.KEYUP:
            # 角色切换
            if event.key == pygame.K_LEFT:
                hero_type = (self.player.hero_type - 1) % 3
                self.player.change_hero(hero_type)
            elif event.key == pygame.K_RIGHT:
                hero_type = (self.player.hero_type + 1) % 3
                self.player.change_hero(hero_type)
            # 技能释放
            elif event.key == pygame.K_x:
                if not self.is_frozen and self.boom_count > 0:
                    self.freeze_enemy()

        # 处理鼠标事件
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键射击
                self.player.shoot()
            elif event.button == 3:  # 右键切换角色
                hero_type = (self.player.hero_type + 1) % 3
                self.player.change_hero(hero_type)

        # 处理自定义事件
        elif event.type == HERO_ATTACK:
            self.shoot(**event.dict)
        elif event.type == ENEMY_ESCAPED:  # 敌人逃逸
            enemy = event.dict.get('enemy', None)
            damage = event.dict.get('damage', 0)
            if enemy:
                self.hp -= damage
                self.hp_bar.set_progress(self.hp)
                self.effects_manager.add_effect(0, enemy.rect.centery, RED)
                if self.hp <= 0:
                    self.parent.game_over()

        elif event.type == ENEMY_KILLED:  # 敌人击杀
            enemy = event.dict.get('enemy', None)
            if enemy:
                self.kill_count += 1
                self.mp += 10
                self.mp_bar.set_progress(self.mp)
                self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)
                self.effects_manager.add_effect(enemy.rect.x, enemy.rect.centery, GREEN)

                # 每击杀10个敌人获得一个技能点
                if self.kill_count % 10 == 0:
                    self.mp = 0
                    self.mp_bar.set_progress(self.mp)
                    self.boom_count += 1
                    self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)

        # 更新UI精灵
        self.ui_sprites.update(event)
