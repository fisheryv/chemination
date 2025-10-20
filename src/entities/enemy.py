import random

import pygame

from src.config.settings import RED, SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 创建敌人动画帧
        self.frames = []
        for i in range(4):
            surf = pygame.Surface((60, 50), pygame.SRCALPHA)
            pygame.draw.rect(surf, RED, (0, 0, 60, 50), border_radius=8)
            pygame.draw.rect(surf, (200, 0, 0), (15, 10, 30, 15), border_radius=5)  # 头部
            pygame.draw.rect(surf, (200, 0, 0), (20, 30, 20, 15), border_radius=3)  # 身体

            # 添加一些变化来模拟行走
            if i % 2 == 0:
                pygame.draw.rect(surf, (200, 0, 0), (10, 35, 10, 10), border_radius=3)  # 左腿
                pygame.draw.rect(surf, (200, 0, 0), (40, 30, 10, 15), border_radius=3)  # 右腿
            else:
                pygame.draw.rect(surf, (200, 0, 0), (10, 30, 10, 15), border_radius=3)  # 左腿
                pygame.draw.rect(surf, (200, 0, 0), (40, 35, 10, 10), border_radius=3)  # 右腿
            self.frames.append(surf)

        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # 从屏幕右侧随机位置生成
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)

        self.speed = random.randint(2, 5)
        self.health = 3

    def update(self):
        self.rect.x -= self.speed

        # 动画更新
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # 如果敌人离开屏幕左侧，则删除
        if self.rect.right < 0:
            self.kill()

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
