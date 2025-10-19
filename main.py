import pygame
import sys

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, load_settings, get_option
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
    load_settings()
    _intro = get_option("game", "intro")
    if _intro == "on":
        from src.story.intro import play_story
        print("Tell the game story")
        play_story(screen)

    from src.game.game import Game
    print("Game module imported")
    game = Game(screen)
    print("Game instance created")
    game.run()

if __name__ == "__main__":
    main()