import random
import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, ENEMY_ESCAPED, ENEMY_KILLED
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_row, resource_path


class Enemy(pygame.sprite.Sprite):
    """敌人类"""
    def __init__(self, name, params):
        """
        初始化敌人
        
        Args:
            name (str): 敌人名称（化学式）
            params (dict): 敌人参数（类型、血量、速度）
        """
        super().__init__()
        self.name = name
        self.params = params
        
        # 加载敌人动画帧
        try:
            self.frames = load_sprite_row(f"assets/images/enemy/{name}.png", 4, scale=1)
        except pygame.error:
            # 如果无法加载图片，创建一个默认的矩形作为替代
            self.frames = [pygame.Surface((50, 50), pygame.SRCALPHA)]
            self.frames[0].fill((200, 100, 100, 200))
        
        # 加载血量图标
        try:
            self.heart1 = pygame.image.load(resource_path("assets/images/ui/heart1.png"))
            self.heart3 = pygame.image.load(resource_path("assets/images/ui/heart3.png"))
        except pygame.error:
            # 如果无法加载图片，创建简单的替代图形
            self.heart1 = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.heart1.fill((255, 0, 0, 128))
            self.heart3 = pygame.Surface((20, 20), pygame.SRCALPHA)
            self.heart3.fill((0, 255, 0, 128))

        # 动画相关属性
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # 位置初始化（从屏幕右侧随机位置生成）
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(120, SCREEN_HEIGHT - 120 - self.rect.height)

        # 物理属性
        self.speed = params["speed"]
        self.health = params["hp"]
        self.type = params["type"]

        # 渲染敌人名称
        font = pygame.font.SysFont(None, 24)
        self.name_surface = font.render(self.name, True, WHITE)
        
        # 冻结状态
        self.is_freeze = False

    def freeze(self):
        """冻结敌人"""
        self.is_freeze = True

    def unfreeze(self):
        """解冻敌人"""
        self.is_freeze = False

    def update(self):
        """更新敌人状态"""
        # 如果被冻结，不更新位置
        if self.is_freeze:
            return
            
        # 更新位置
        self.rect.x -= self.speed

        # 更新动画帧
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        
        # 边界检查：如果敌人离开屏幕左侧，则触发逃脱事件并删除
        if self.rect.right < 0:
            # 触发敌人逃脱事件
            pygame.event.post(pygame.event.Event(ENEMY_ESCAPED, {
                'enemy': self,
                'damage': self.health
            }))
            # 删除敌人
            self.kill()

    def draw_hp(self, screen):
        """
        绘制敌人血量
        
        Args:
            screen (pygame.Surface): 屏幕表面
        """
        # 绘制血量图标
        _x = self.rect.x + (self.rect.width - self.heart1.get_width() * self.params["hp"]) / 2
        for i in range(self.params["hp"]):
            heart_image = self.heart3 if i < self.health else self.heart1
            screen.blit(heart_image, (_x + i * self.heart3.get_width(), self.rect.y - self.heart3.get_height()))
        
        # 绘制敌人名称
        _x = self.rect.x + (self.rect.width - self.name_surface.get_width()) / 2
        screen.blit(self.name_surface, (_x, self.rect.bottom))

    def take_damage(self, bullet_type):
        """
        敌人受到伤害
        
        Args:
            bullet_type (BulletType): 子弹类型
        """
        # 判断是否受到伤害
        if bullet_type == BulletType.ACID:
            _damage = self.type == "metal" or self.type == "base"
        elif bullet_type == BulletType.BASE:
            _damage = self.type == "acid"
        else:  # BulletType.METAL
            _damage = self.type == "salt"
            
        # 如果受到伤害，减少血量
        if _damage:
            self.health -= 1
            if self.health <= 0:
                # 触发敌人击杀事件
                pygame.event.post(pygame.event.Event(ENEMY_KILLED, {
                    'enemy': self,
                    'damage': 0
                }))
                # 删除敌人
                self.kill()
