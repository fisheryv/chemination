import os
import sys

import pygame
from pygame import BLEND_RGBA_MULT


def create_alpha_image(image, alpha):
    """创建具有指定透明度的图像副本"""
    alpha_image = image.copy()
    alpha_image.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
    return alpha_image


def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后环境"""
    try:
        # PyInstaller 创建临时文件夹，将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 精灵图分割函数
def load_sprite_sheet(filename, rows, cols, directions=('down', 'left', 'right', 'up'), scale=1):
    """从精灵图中加载并分割所有帧"""
    filepath = resource_path(filename)
    sprite_sheet = pygame.image.load(filepath).convert_alpha()
    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height() // rows

    frames = {}

    for row in range(rows):
        direction_frames = []
        for col in range(cols):
            frame = sprite_sheet.subsurface(
                pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            )
            if scale != 1:
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)
                frame = pygame.transform.scale(frame, (new_width, new_height))
            direction_frames.append(frame)
        frames[directions[row]] = direction_frames

    return frames


# 精灵图(单行)分割函数
def load_sprite_row(filename, cols, scale=1):
    """从精灵图中加载并分割所有帧"""
    filepath = resource_path(filename)
    sprite_sheet = pygame.image.load(filepath).convert_alpha()
    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height()

    direction_frames = []
    for col in range(cols):
        frame = sprite_sheet.subsurface(
            pygame.Rect(col * frame_width, 0, frame_width, frame_height)
        )
        if scale != 1:
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)
            frame = pygame.transform.scale(frame, (new_width, new_height))
        direction_frames.append(frame)
    return direction_frames
