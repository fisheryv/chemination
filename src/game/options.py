import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD, WHITE
from src.entities.button import ImageButton
from src.entities.switcher import Switcher
from src.game.scene import Scene

option_text = [
    "Music:",
    "Skip Intro:"
]


class OptionsScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load("assets/images/ui/options_bg.jpg")  # 背景图
        self.img = pygame.image.load("assets/images/ui/placeholder.jpg")  # 装饰图
        self.img = pygame.transform.scale(self.img, (400, 400))
        try:
            font = pygame.font.Font("assets/fonts/PixelEmulator.ttf", 28)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            font = pygame.font.SysFont(None, 28)
        self.line_surfaces = []
        for line in option_text:
            line_surface = font.render(line, True, WHITE)
            self.line_surfaces.append(line_surface)

        button_width = 50
        button_height = 50
        _x = 20
        _y = 30
        button_back = ImageButton("assets/images/ui/back_arrow.png",
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)
        button_width = 127
        button_height = 60
        _x = 900
        _y = 150
        music_switcher = Switcher(_x, _y, button_width, button_height,
                                  action=self.parent.music_toggle)

        _y = _y + 100
        intro_switcher = Switcher(_x, _y, button_width, button_height,
                                  action=self.parent.intro_toggle)
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        # 将按钮添加到精灵组
        self.all_sprites.add(button_back, music_switcher, intro_switcher)

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.img, (150, 120))
        current_y = 160
        for line_surface in self.line_surfaces:
            line_x = 880 - line_surface.get_width()
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + 70  # 5像素行间距
        self.all_sprites.draw(screen)

    def process_input(self, event):
        self.all_sprites.update(event)
