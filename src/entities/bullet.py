from enum import Enum
import pygame

from src.config.settings import SCREEN_WIDTH
from src.utils.tools import load_sprite_row


class BulletType(Enum):
    """子弹类型枚举"""
    ACID = "acid"
    BASE = "base"
    METAL = "metal"


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    def __init__(self, x: int, y: int, direction: int, bullet_type: BulletType):
        """
        初始化子弹
        
        Args:
            x (int): 子弹初始x坐标
            y (int): 子弹初始y坐标
            direction (int): 子弹方向 (-1: 左, 1: 右)
            bullet_type (BulletType): 子弹类型
        """
        super().__init__()
        self.bullet_type = bullet_type

        # 加载子弹动画帧
        self.frames = load_sprite_row(
            f"assets/images/spirits/{self.bullet_type.value}.png",
            3,
            scale=1
        )

        # 动画相关属性
        self.current_frame = 0
        self.animation_speed = 0.3
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # 物理属性
        self.speed = 10
        self.direction = direction

        # 根据方向翻转图像
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        """更新子弹位置和动画"""
        # 更新位置
        self.rect.x += self.speed * self.direction

        # 更新动画帧
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # 根据方向翻转图像
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # 边界检查：如果子弹飞出屏幕则删除
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
