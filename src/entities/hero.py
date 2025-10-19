from typing import Optional

import pygame
from pygame.locals import *
from src.config.settings import BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.bullet import Bullet, BulletType
from src.utils.tools import load_sprite_sheet, load_sprite_sheet2

HEROS = ["hero5", "hero6", "hero8"]
BULLET_TYPES = [BulletType.ACID, BulletType.BASE, BulletType.METAL]


class Hero(pygame.sprite.Sprite):
    """玩家角色类"""

    def __init__(self, battle_scene):
        super().__init__()
        self.battle_scene = battle_scene
        self.hero_type = 0
        # 从精灵图加载所有方向的动画帧，精灵图的顺序是下、上、左、右
        self.animations = load_sprite_sheet2(HEROS[self.hero_type] + ".png", 3, 4, scale=1)
        # 从精灵图加载攻击动画
        self.attack = load_sprite_sheet(HEROS[self.hero_type] + '_attack.png', 1, 4, directions=["attack"], scale=1)
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.speed = 5
        self.last_shot = 0
        self.shoot_delay = 300  # 毫秒

        self.walking = False
        self.direction = 1  # 1 向右, -1 向左

        self.attacking = False

    def change_hero(self, hero_type):
        self.hero_type = hero_type
        hero = HEROS[self.hero_type]
        old_center = self.rect.center
        self.animations = load_sprite_sheet2(hero + ".png", 3, 4, scale=1)
        self.attack = load_sprite_sheet(hero + '_attack.png', 1, 4, directions=["attack"], scale=1)
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        if self.attacking:
            self.current_frame += 0.25
            if self.current_frame >= len(self.attack["attack"]):
                self.current_frame = 0
                self.attacking = False
                self.battle_scene.shoot(self.rect.centerx, self.rect.centery, self.direction, BULLET_TYPES[self.hero_type])
            self.image = self.attack["attack"][int(self.current_frame)]
            return
        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 切换角色
        if keys[K_1]:
            self.change_hero(0)
        elif keys[K_2]:
            self.change_hero(1)
        elif keys[K_3]:
            self.change_hero(2)

        # 移动
        self.walking = False
        # if keys[K_LEFT] or keys[K_a]:
        #     self.current_direction = 'left'
        #     self.rect.x -= self.speed
        #     self.walking = True
        # if keys[K_RIGHT] or keys[K_d]:
        #     self.current_direction = 'right'
        #     self.rect.x += self.speed
        #     self.walking = True
        if keys[K_UP] or keys[K_w]:
            self.current_direction = 'up'
            self.rect.y -= self.speed
            self.walking = True
        if keys[K_DOWN] or keys[K_s]:
            self.current_direction = 'down'
            self.rect.y += self.speed
            self.walking = True

        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # 动画更新
        if self.walking:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.animations[self.current_direction]):
                self.current_frame = 0
            self.image = self.animations[self.current_direction][int(self.current_frame)]
        else:
            # 空闲时使用第一帧
            self.image = self.animations[self.current_direction][0]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.attacking = True
            self.current_frame = 0
            self.current_direction = "right"
