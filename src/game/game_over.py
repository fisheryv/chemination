import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.button import ImageButton
from src.game.scene import Scene
from src.utils.tools import resource_path


class GameOverScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load(resource_path("assets/images/ui/gameover_bg.jpg"))  # 背景图

        button_width = 270 * 0.6
        button_height = 110 * 0.6
        _x = (SCREEN_WIDTH - button_width) // 2
        _y = SCREEN_HEIGHT - button_height - 50
        button_continue = ImageButton(resource_path("assets/images/ui/menu_continue.png"),
                                      _x, _y, button_width, button_height,
                                      action=self.parent.main_menu)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        # 将按钮添加到精灵组
        self.all_sprites.add(button_continue)

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen)

    def process_input(self, event):
        self.all_sprites.update(event)
