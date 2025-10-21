import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, load_settings
from src.utils.tools import resource_path


def main():
    """主函数"""
    pygame.init()
    pygame.mixer.init()  # 初始化音频模块
    # 加载图标文件并创建Surface对象
    icon = pygame.image.load(resource_path("icon.ico"))
    # 设置窗口的新图标
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    print("Pygame initialized")
    # 加载设置
    load_settings()
    # 进入游戏主循环
    from src.game.game import Game
    print("Game module imported")
    game = Game(screen)
    print("Game instance created")
    game.run()


if __name__ == "__main__":
    main()
