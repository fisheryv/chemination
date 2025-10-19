import pygame

from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.entities.hero import Hero
from src.game.scene import Scene
from src.utils.music import load_background_music, play_background_music
from src.utils.tools import resource_path


class BattleScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load(resource_path("assets/images/battle/battle_bg1.jpg"))  # 背景图
        self.img = pygame.image.load(resource_path("assets/images/ui/placeholder.jpg"))  # 装饰图
        self.img = pygame.transform.scale(self.img, (400, 400))
        try:
            font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 28)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            font = pygame.font.SysFont(None, 28)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # 创建玩家
        self.player = Hero(self)
        self.all_sprites.add(self.player)

        self.enemy_spawn_timer = 0

        # 加载背景音乐
        load_background_music("battle_bgm.mp3")
        # play_background_music()

    def spawn_enemy(self):
        """
        生成敌人
        """
        enemy = Enemy()
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def shoot(self, x, y, direction, bullet_type):
        bullet = Bullet(x, y, direction, bullet_type)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self):
        # 生成敌人
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 60:  # 每60帧生成一个敌人
            self.spawn_enemy()
            self.enemy_spawn_timer = 0

        # 更新精灵
        self.all_sprites.update()

        # 碰撞检测：子弹与敌人
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage()

    def render(self, screen):
        # 绘制背景
        screen.blit(self.background, (0, 0))
        # 绘制所有精灵
        self.all_sprites.draw(screen)

    def process_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()
