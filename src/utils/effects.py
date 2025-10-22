import pygame
import random


class Particle:
    """粒子类"""

    def __init__(self, x: float, y: float, dx: float, dy: float, size: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.ds = self.size / 30.0

    def is_alive(self):
        """判断粒子是否存活"""
        return self.size > 0

    def update(self):
        """更新粒子位置"""
        if self.is_alive():
            self.dx *= 0.95
            self.dy *= 0.95
            self.x += self.dx
            self.y += self.dy
            self.size -= self.ds

    def draw(self, screen: pygame.Surface, color: tuple):
        """绘制粒子"""
        if self.is_alive():
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))


class Effect:
    """特效类"""

    def __init__(self, x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color
        self.timer = 30  # 特效持续帧数
        self.particles: list[Particle] = []

        # 创建粒子
        for i in range(10):
            particle = Particle(x, y, random.uniform(-8, 8), random.uniform(-8, 8), random.randint(5, 10))
            self.particles.append(particle)

    def is_alive(self):
        """判断特效是否存活"""
        return self.timer > 0

    def update(self):
        """更新特效"""
        self.timer -= 1
        if self.timer > 0:
            # 更新粒子位置
            for particle in self.particles:
                particle.update()

    def draw(self, screen: pygame.Surface):
        """绘制特效"""
        for particle in self.particles:
            particle.draw(screen, self.color)


class EffectsManager:
    """特效管理器"""

    def __init__(self):
        self.effects: list[Effect] = []  # 存储特效信息

    def add_effect(self, x: int, y: int, color: tuple):
        """添加特效"""
        effect = Effect(x, y, color)
        self.effects.append(effect)

    def update_effects(self):
        """更新特效"""
        for effect in self.effects:
            effect.timer -= 1
            if effect.is_alive():
                effect.update()
        self.effects = [effect for effect in self.effects if effect.is_alive()]

    def draw_effects(self, screen: pygame.Surface):
        """绘制特效"""
        for effect in self.effects:
            effect.draw(screen)
