import pygame
from pygame.locals import *
from src.config.settings import SCREEN_HEIGHT
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_sheet, load_sprite_row

BULLET_TYPES = [BulletType.BASE, BulletType.ACID, BulletType.METAL]


class Avatar:
    def __init__(self, hero_type):
        self.hero_type = hero_type
        # 从精灵图加载所有方向的动画帧，精灵图的顺序是下、左、上
        self.animations = load_sprite_sheet(f"assets/images/spirits/hero{self.hero_type + 1}.png",
                                            3, 4, directions=["down", "left", "up"], scale=1)
        # 通过水平镜像生成向右行走帧
        direction_frames = []
        for f in self.animations["left"]:
            direction_frames.append(pygame.transform.flip(f, True, False))
        self.animations["right"] = direction_frames
        # 攻击动画
        self.attack = load_sprite_row(f"assets/images/spirits/hero{self.hero_type + 1}_attack.png", 4,
                                      scale=1)


class Hero(pygame.sprite.Sprite):
    """玩家角色类"""

    def __init__(self, battle_scene):
        super().__init__()
        self.battle_scene = battle_scene
        self.hero_type = 0
        self.avatars = [Avatar(0), Avatar(1), Avatar(2)]
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
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
        old_center = self.rect.center
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        if self.attacking:
            self.current_frame += 0.25
            if self.current_frame >= len(self.avatars[self.hero_type].attack):
                self.current_frame = 0
                self.attacking = False
                self.battle_scene.shoot(self.rect.centerx, self.rect.centery, self.direction,
                                        BULLET_TYPES[self.hero_type])
            self.image = self.avatars[self.hero_type].attack[int(self.current_frame)]
            return
        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 切换角色
        if keys[K_1]:
            self.hero_type = 0
            self.change_hero(0)
        elif keys[K_2]:
            self.hero_type = 1
            self.change_hero(1)
        elif keys[K_3]:
            self.hero_type = 2
            self.change_hero(2)

        # 移动
        self.walking = False
        # if keys[K_LEFT] or keys[K_a]:
        # self.current_direction = 'left'
        # self.rect.x -= self.speed
        # self.walking = True
        # if keys[K_RIGHT] or keys[K_d]:
        # self.current_direction = 'right'
        # self.rect.x += self.speed
        # self.walking = True
        if keys[K_UP] or keys[K_w]:
            self.current_direction = 'up'
            self.rect.y -= self.speed
            self.walking = True
        if keys[K_DOWN] or keys[K_s]:
            self.current_direction = 'down'
            self.rect.y += self.speed
            self.walking = True

        # 边界检查
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH
        if self.rect.top < 120:
            self.rect.top = 120
        if self.rect.bottom > SCREEN_HEIGHT - 120:
            self.rect.bottom = SCREEN_HEIGHT - 120

        # 动画更新
        if self.walking:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.avatars[self.hero_type].animations[self.current_direction]):
                self.current_frame = 0
            self.image = self.avatars[self.hero_type].animations[self.current_direction][int(self.current_frame)]
        else:
            # 空闲时使用第一帧
            self.image = self.avatars[self.hero_type].animations[self.current_direction][0]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.attacking = True
            self.current_frame = 0
            self.current_direction = "right"
