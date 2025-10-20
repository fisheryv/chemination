from enum import Enum

import pygame

from src.config.settings import GREEN, SCREEN_WIDTH
from src.utils.tools import load_sprite_sheet, load_sprite_row


class BulletType(Enum):
    ACID = "acid"
    BASE = "base"
    METAL = "metal"


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_type):
        super().__init__()
        self.bullet_type = bullet_type
        # 创建子弹动画帧
        self.frames = load_sprite_row(f"assets/images/spirits/{self.bullet_type.value}.png", 3, scale=1)

        self.current_frame = 0
        self.animation_speed = 0.3
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 10
        self.direction = direction

        # 根据方向翻转图像
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.x += self.speed * self.direction

        # 动画更新
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # 根据方向翻转图像
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # 如果子弹飞出屏幕，则删除
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
