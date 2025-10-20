import pygame
import random
from src.config.settings import GRAY, DARK_GRAY, RED, DARK_RED, BLUE, DARK_BLUE, GREEN, DARK_GREEN, BLACK
from src.utils.tools import resource_path


class ProcessBar:
    """进度条组件"""

    def __init__(self, x, y, width, height, border_color, bg_color, icon=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_color = border_color
        self.bg_color = bg_color
        self.icon = icon
        if self.icon:
            self.icon = pygame.image.load(resource_path("assets/images/ui/" + self.icon))
            self.icon = pygame.transform.scale(self.icon, (self.height, self.height))
        self.progress = 100
        self.size = self.height // 6
        self.bar_w = self.width - self.size * 6
        self.bar_x = self.x + self.size * 3
        self.bar_y = self.y + self.size * 2
        self.bar_h = self.size * 2

    def set_progress(self, progress):
        """设置进度"""
        self.progress = progress
        if self.progress < 0:
            self.progress = 0
        elif self.progress > 100:
            self.progress = 100
        self.bar_w = (self.width - self.size * 8) * progress / 100

    def get_progress(self):
        """获取进度"""
        return self.progress

    def draw(self, screen):
        _x_offset = 0
        if self.icon:
            screen.blit(self.icon, (self.x, self.y))
            _x_offset = self.height
        # 绘制进度条外框
        _h = self.size
        for i in range(2):
            _x = _x_offset + self.x + i * self.size
            _y = self.y + 2 * self.size - i * self.size
            _w = self.width - i * self.size * 2 - _x_offset
            pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
            pygame.draw.rect(screen, self.bg_color, (_x + self.size, _y, _w - self.size * 2, _h))
            _y = self.y + 3 * self.size + i * self.size
            pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
            pygame.draw.rect(screen, self.bg_color, (_x + self.size, _y, _w - self.size * 2, _h))

        _x = self.x + self.size * 2 + _x_offset
        _y = self.y
        _w = self.width - self.size * 4 - _x_offset
        pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))
        _y = self.y + 5 * self.size
        pygame.draw.rect(screen, self.border_color, (_x, _y, _w, _h))

        # 绘制进度
        pygame.draw.rect(screen, self.border_color,
                         (self.bar_x + _x_offset, self.bar_y, self.bar_w - _x_offset, self.bar_h))
