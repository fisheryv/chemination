import pygame

from src.config.settings import SCREEN_WIDTH, GOLD, WHITE
from src.entities.button import ImageButton
from src.game.scene import Scene

credits_text = [
    "Producer:", "Fisher, Lucas",
    "Scriptwriter:", "Fisher",
    "Programmer:", "Fisher, Qwen-Coder-3",
    "Artist:", "FLUX, PD_PixelCraft, Qwen-Image",
    "Music:", '"The Ring of Load"'
]


class CreditsScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load("assets/images/ui/credits_bg.jpg")  # 背景图
        try:
            font1 = pygame.font.Font("assets/fonts/PixelEmulator.ttf", 28)
            font2 = pygame.font.Font("assets/fonts/PixelEmulator.ttf", 28)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            font1 = pygame.font.SysFont(None, 28)
            font2 = pygame.font.SysFont(None, 28)
        font1.set_underline(True)
        self.line_surfaces = []
        for i, line in enumerate(credits_text):
            if i % 2 == 0:
                line_surface = font1.render(line, True, GOLD)
            else:
                line_surface = font2.render(line, True, WHITE)
            self.line_surfaces.append(line_surface)

        button_width = 50
        button_height = 50
        _x = 20
        _y = 30
        button_back = ImageButton("assets/images/ui/back_arrow.png",
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        # 将按钮添加到精灵组
        self.all_sprites.add(button_back)

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        current_y = 80
        for i, line_surface in enumerate(self.line_surfaces):
            line_x = (SCREEN_WIDTH - line_surface.get_width()) // 2
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + (10 if i % 2 == 0 else 30)  # 5像素行间距
        self.all_sprites.draw(screen)

    def process_input(self, event):
        self.all_sprites.update(event)
