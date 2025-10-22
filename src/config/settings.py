import configparser
import os
import pygame

from src.utils.tools import resource_path

# 游戏基本信息
GAME_NAME = "Chemination"
VERSION = "0.1.0"

# 游戏窗口设置
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 0)
GOLD = (218, 165, 32)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
DARK_RED = (128, 52, 52)
DARK_BLUE = (52, 95, 130)
DARK_GREEN = (77, 127, 52)
PINK = (229, 71, 130)
CYAN = (65, 166, 220)

# 自定义事件
ENEMY_ESCAPED = pygame.USEREVENT + 1  # 敌人逃脱事件
ENEMY_KILLED = pygame.USEREVENT + 2  # 敌人击杀事件
HERO_ATTACK = pygame.USEREVENT + 3  # 英雄攻击事件

# 默认设置选项
OPTIONS = {
    "game": {
        "intro": "on",
        "music": "on",
    }
}

# 配置文件路径
config_file = resource_path("setting.ini")
config = configparser.ConfigParser()


def load_settings():
    """从INI文件加载设置"""
    try:
        if os.path.exists(config_file):
            config.read(config_file)
        else:
            # 如果文件不存在，创建默认设置
            for section, options in OPTIONS.items():
                config[section] = options
            save_settings()
    except Exception as e:
        print(f"加载设置时出错: {e}")


def save_settings():
    """保存设置到INI文件"""
    try:
        with open(config_file, 'w') as f:
            config.write(f)
    except Exception as e:
        print(f"保存设置时出错: {e}")


def get_option(section: str, key: str) -> str | None:
    """获取设置值"""
    try:
        return config.get(section, key)
    except:
        return None


def set_option(section: str, key: str, value):
    """设置值"""
    if section not in config:
        config[section] = {}
    config[section][key] = str(value)
