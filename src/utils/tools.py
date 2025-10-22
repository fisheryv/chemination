import os
import sys

import pygame
from pygame import BLEND_RGBA_MULT
from pathlib import Path


def create_alpha_image(image, alpha):
    """
    创建具有指定透明度的图像副本
    
    Args:
        image (pygame.Surface): 原始图像
        alpha (int): 透明度值 (0-255)
        
    Returns:
        pygame.Surface: 带有指定透明度的新图像
    """
    alpha_image = image.copy()
    alpha_image.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
    return alpha_image


def resource_path(relative_path: str):
    """
    获取资源的绝对路径，兼容开发环境和打包后环境
    
    Args:
        relative_path (str): 相对路径
        
    Returns:
        str: 资源的绝对路径
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 创建临时文件夹，将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
        print("_MEIPASS = " + base_path)
    elif __file__ is not None:
        # In Nuitka onefile mode, __file__ for the main module points to the temporary extraction location.
        current_path = Path(__file__).resolve()
        parent_path = current_path.parent
        base_path = parent_path.parent.parent
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_sprite_sheet(filename: str, rows: int, cols: int,
                      directions: tuple = ('down', 'left', 'right', 'up'),
                      scale: float = 1.0) -> dict[str, list[pygame.Surface]]:
    """
    从精灵图中加载并分割所有帧（多行精灵图）
    
    Args:
        filename (str): 精灵图文件路径
        rows (int): 精灵图行数
        cols (int): 精灵图列数
        directions (tuple): 方向标签
        scale (float): 缩放比例
        
    Returns:
        dict: 按方向分组的帧列表
    """
    try:
        filepath = resource_path(filename)
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
    except pygame.error as e:
        print(f"无法加载精灵图 {filename}: {e}")
        # 创建一个简单的替代精灵图
        sprite_sheet = pygame.Surface((cols * 50, rows * 50), pygame.SRCALPHA)
        sprite_sheet.fill((200, 100, 100, 200))

    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height() // rows

    frames = {}

    for row in range(rows):
        direction_frames = []
        for col in range(cols):
            try:
                frame = sprite_sheet.subsurface(
                    pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                )
            except ValueError:
                # 如果子表面超出范围，创建一个默认帧
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.fill((100, 200, 100, 200))

            # 缩放帧
            if scale != 1:
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)
                frame = pygame.transform.scale(frame, (new_width, new_height))
            direction_frames.append(frame)

        # 确保方向标签不超出范围
        direction_key = directions[row] if row < len(directions) else f"direction_{row}"
        frames[direction_key] = direction_frames

    return frames


def load_sprite_row(filename: str, cols: int, scale: float = 1.0) -> list[pygame.Surface]:
    """
    从精灵图中加载并分割所有帧（单行精灵图）
    
    Args:
        filename (str): 精灵图文件路径
        cols (int): 精灵图列数
        scale (float): 缩放比例
        
    Returns:
        list: 帧列表
    """
    try:
        filepath = resource_path(filename)
        sprite_sheet = pygame.image.load(filepath).convert_alpha()
    except pygame.error as e:
        print(f"无法加载精灵图 {filename}: {e}")
        # 创建一个简单的替代精灵图
        sprite_sheet = pygame.Surface((cols * 50, 50), pygame.SRCALPHA)
        sprite_sheet.fill((100, 100, 200, 200))

    frame_width = sprite_sheet.get_width() // cols
    frame_height = sprite_sheet.get_height()

    direction_frames = []
    for col in range(cols):
        try:
            frame = sprite_sheet.subsurface(
                pygame.Rect(col * frame_width, 0, frame_width, frame_height)
            )
        except ValueError:
            # 如果子表面超出范围，创建一个默认帧
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.fill((100, 200, 100, 200))

        # 缩放帧
        if scale != 1:
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)
            frame = pygame.transform.scale(frame, (new_width, new_height))
        direction_frames.append(frame)

    return direction_frames
