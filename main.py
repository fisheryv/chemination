import pygame
import sys

def main():
    """主函数"""
    pygame.init()
    pygame.mixer.init()  # 初始化音频模块
    print("Pygame initialized")
    from src.game.game import Game
    print("Game module imported")
    game = Game()
    print("Game instance created")
    game.run()

if __name__ == "__main__":
    main()