import pygame
import sys

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, load_settings
from src.utils.tools import resource_path


def main():
    """主函数"""
    # 初始化Pygame
    pygame.init()
    pygame.mixer.init()  # 初始化音频模块
    
    try:
        # 设置窗口图标
        icon = pygame.image.load(resource_path("icon.ico"))
        pygame.display.set_icon(icon)
    except pygame.error:
        print("警告: 无法加载图标文件 icon.ico")
    
    # 创建游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    
    # 加载设置
    load_settings()
    
    # 导入并运行游戏主类
    try:
        from src.game.game import Game
        game = Game(screen)
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
