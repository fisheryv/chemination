import pygame
from pygame.locals import *

from src.config.settings import SCREEN_HEIGHT, HERO_ATTACK
from src.entities.bullet import BulletType
from src.utils.tools import load_sprite_sheet, load_sprite_row

# 子弹类型映射
BULLET_TYPES = [BulletType.BASE, BulletType.ACID, BulletType.METAL]


class Avatar:
    """玩家角色外观类"""

    def __init__(self, hero_type: int):
        """
        初始化角色外观
        
        Args:
            hero_type (int): 角色类型 (0: 碱, 1: 酸, 2: 盐)
        """
        self.hero_type = hero_type

        # 加载行走动画帧（下、左、上方向）
        try:
            self.animations = load_sprite_sheet(
                f"assets/images/spirits/hero{self.hero_type + 1}.png",
                3, 4,
                directions=("down", "left", "up"),
                scale=1
            )
        except pygame.error:
            # 如果无法加载图片，创建简单的替代图形
            self.animations = self._create_default_animations()

        # 通过水平镜像生成向右行走帧
        direction_frames = []
        for f in self.animations["left"]:
            direction_frames.append(pygame.transform.flip(f, True, False))
        self.animations["right"] = direction_frames

        # 加载攻击动画
        try:
            self.attack = load_sprite_row(
                f"assets/images/spirits/hero{self.hero_type + 1}_attack.png",
                4,
                scale=1
            )
        except pygame.error:
            # 如果无法加载攻击动画，使用行走动画的第一帧作为替代
            self.attack = self.animations["right"][:4] if len(self.animations["right"]) >= 4 else [self.animations[
                                                                                                       "right"][0]] * 4

    def _create_default_animations(self):
        """创建默认动画帧"""
        # 创建一个简单的彩色矩形作为默认角色外观
        default_frames = []
        colors = [(100, 100, 255), (100, 255, 100), (255, 100, 100)]  # 蓝、绿、红
        for color in colors:
            frame = pygame.Surface((50, 80), pygame.SRCALPHA)
            frame.fill((*color, 200))  # 添加透明度
            default_frames.append(frame)

        # 将帧分配给不同方向
        return {
            "down": [default_frames[0]],
            "left": [default_frames[1]],
            "up": [default_frames[2]],
            "right": [default_frames[1]]  # 右方向使用左方向的镜像
        }


class Hero(pygame.sprite.Sprite):
    """玩家角色类"""

    def __init__(self):
        """
        初始化玩家角色
        """
        super().__init__()
        self.hero_type = 0  # 默认角色类型（碱类）

        # 创建角色外观实例
        self.avatars = [Avatar(0), Avatar(1), Avatar(2)]

        # 动画相关属性
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        # 物理属性
        self.speed = 5
        self.last_shot = 0
        self.shoot_delay = 300  # 毫秒

        # 状态属性
        self.walking = False
        self.direction = 1  # 1 向右, -1 向左
        self.attacking = False

    def change_hero(self, hero_type: int):
        """
        切换角色类型
        
        Args:
            hero_type (int): 新的角色类型
        """
        self.hero_type = hero_type
        old_center = self.rect.center
        self.current_direction = 'right'
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.avatars[self.hero_type].animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        """更新角色状态"""
        # 处理攻击动画
        if self.attacking:
            self.current_frame += 0.25
            if self.current_frame >= len(self.avatars[self.hero_type].attack):
                self.current_frame = 0
                self.attacking = False
                # 触发攻击事件
                pygame.event.post(pygame.event.Event(HERO_ATTACK, {
                    'x': self.rect.centerx,
                    'y': self.rect.centery,
                    'direction': self.direction,
                    'bullet_type': BULLET_TYPES[self.hero_type]
                }))
            self.image = self.avatars[self.hero_type].attack[int(self.current_frame)]
            return

        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 切换角色类型
        if keys[K_1]:
            self.change_hero(0)  # 碱类
        elif keys[K_2]:
            self.change_hero(1)  # 酸类
        elif keys[K_3]:
            self.change_hero(2)  # 盐类

        # 处理移动
        self.walking = False

        # 水平移动（已注释，如需启用可取消注释）
        # if keys[K_LEFT] or keys[K_a]:
        #     self.current_direction = 'left'
        #     self.rect.x -= self.speed
        #     self.walking = True
        #     self.direction = -1
        # if keys[K_RIGHT] or keys[K_d]:
        #     self.current_direction = 'right'
        #     self.rect.x += self.speed
        #     self.walking = True
        #     self.direction = 1

        # 垂直移动
        if keys[K_UP] or keys[K_w]:
            self.current_direction = 'up'
            self.rect.y -= self.speed
            self.walking = True
        if keys[K_DOWN] or keys[K_s]:
            self.current_direction = 'down'
            self.rect.y += self.speed
            self.walking = True

        # 边界检查
        # 限制水平移动边界（如需启用可取消注释）
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH

        # 限制垂直移动边界
        if self.rect.top < 120:
            self.rect.top = 120
        if self.rect.bottom > SCREEN_HEIGHT - 120:
            self.rect.bottom = SCREEN_HEIGHT - 120

        # 更新动画帧
        if self.walking:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.avatars[self.hero_type].animations[self.current_direction]):
                self.current_frame = 0
            self.image = self.avatars[self.hero_type].animations[self.current_direction][int(self.current_frame)]
        else:
            # 空闲时使用第一帧
            self.image = self.avatars[self.hero_type].animations[self.current_direction][0]

    def shoot(self):
        """发射子弹"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.attacking = True
            self.current_frame = 0
            self.current_direction = "right"
