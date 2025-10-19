import configparser
import os

from src.utils.tools import resource_path

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
DARK_RED = (200, 0, 0)
DARK_BLUE = (0, 0, 200)
DARK_GREEN = (0, 200, 0)

OPTIONS = {
    "game": {
        "intro": "on",
        "music": "on",
    }
}
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
        print("设置已保存")
    except Exception as e:
        print(f"保存设置时出错: {e}")


def get_option(section, key):
    """获取设置值"""
    try:
        return config.get(section, key)
    except:
        return None


def set_option(section, key, value):
    """设置值"""
    if section not in config:
        config[section] = {}
    config[section][key] = str(value)
