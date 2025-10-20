import random

import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_row, resource_path


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params
        # 创建敌人动画帧
        self.frames = load_sprite_row(f"assets/images/enemy/{name}.png", 4, scale=1)
        self.heart1 = pygame.image.load(resource_path("assets/images/ui/heart1.png"))
        self.heart3 = pygame.image.load(resource_path("assets/images/ui/heart3.png"))

        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # 从屏幕右侧随机位置生成
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(120, SCREEN_HEIGHT - 120 - self.rect.height)

        self.speed = params["speed"]
        self.health = params["hp"]
        self.type = params["type"]

        font = pygame.font.SysFont(None, 24)
        self.name_surface = font.render(self.name, True, WHITE)

    def update(self):
        self.rect.x -= self.speed

        # 动画更新
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]
        # 如果敌人离开屏幕左侧，则删除
        if self.rect.right < 0:
            # TODO 扣除Hero生命
            self.kill()

    def draw_hp(self, screen):
        _x = self.rect.x + (self.rect.width - self.heart1.get_width() * self.params["hp"]) / 2
        for i in range(self.params["hp"]):
            screen.blit(self.heart3 if i < self.health else self.heart1,
                        (_x + i * self.heart3.get_width(), self.rect.y - self.heart3.get_height()))
        _x = self.rect.x + (self.rect.width - self.name_surface.get_width()) / 2
        screen.blit(self.name_surface, (_x, self.rect.bottom))

    def take_damage(self, bullet_type):
        if bullet_type == BulletType.ACID:
            _damage = self.type == "metal" or self.type == "base"
        elif bullet_type == BulletType.BASE:
            _damage = self.type == "acid"
        else:
            _damage = self.type == "salt"
        if _damage:
            self.health -= 1
            if self.health <= 0:
                self.kill()
