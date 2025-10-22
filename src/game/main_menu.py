import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.button import ImageButton
from src.game.scene import Scene
from src.utils.tools import resource_path


class MainMenuScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load(resource_path("assets/images/ui/menu_bg.jpg"))  # 背景图
        self.game_title = pygame.image.load(resource_path("assets/images/ui/game_title.png"))  # 游戏标题
        self.game_title = pygame.transform.scale(self.game_title, (400, 338))
        button_width = 270 * 0.6
        button_height = 110 * 0.6
        _x = (SCREEN_WIDTH // 2 - button_width) // 2
        _y = SCREEN_HEIGHT - button_height - 50
        button_credits = ImageButton(resource_path("assets/images/ui/menu_credits.png"),
                                     _x, _y, button_width, button_height,
                                     action=self.parent.credits)
        _x = _x + SCREEN_WIDTH // 4
        button_play = ImageButton(resource_path("assets/images/ui/menu_play.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.battle)
        _x = _x + SCREEN_WIDTH // 4
        button_options = ImageButton(resource_path("assets/images/ui/menu_options.png"),
                                     _x, _y, button_width, button_height,
                                     action=self.parent.options)
        button_width, button_height = 50, 50
        _x, _y = 60, 50

        button_help = ImageButton(resource_path("assets/images/ui/menu_help.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.help)
        _x = SCREEN_WIDTH - button_width - _x
        button_close = ImageButton(resource_path("assets/images/ui/menu_close.png"),
                                   _x, _y, button_width, button_height,
                                   action=self.parent.exit_game)
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        # 将按钮添加到精灵组
        self.all_sprites.add(button_play, button_options, button_credits, button_help, button_close)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()
        screen.blit(self.background, (0, 0))
        screen.blit(self.game_title, ((screen_width - self.game_title.get_width()) // 2, 20))
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        self.all_sprites.update(event)
