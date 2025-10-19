import os
import sys

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
