import pygame
import sys

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME


def main():
    """主函数"""
    pygame.init()
    pygame.mixer.init()  # 初始化音频模块
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    print("Pygame initialized")
    # from src.story.intro import play_story
    # print("Tell the game story")
    # play_story(screen)

    from src.game.game import Game
    print("Game module imported")
    game = Game(screen)
    print("Game instance created")
    game.run()

if __name__ == "__main__":
    main()