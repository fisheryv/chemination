import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD, WHITE, DARK_RED, BLACK, DARK_GREEN, DARK_BLUE
from src.entities.button import ImageButton
from src.entities.tab import TabButton
from src.game.scene import Scene
from src.utils.tools import resource_path

goal_text = [
    "Commander Fisher Lucas has 3 heroes,",
    "They are:",
    "",
    "     Base Knight",
    "     who is adept at Base attacks",
    "     and can defeat Acid Monsters.",
    "",
    "     Acid Hitman",
    "     specializes in using Acid",
    "     attacks to defeat Base Monsters.",
    "",
    "     Metal Elf",
    "     can shoot metal arrows to",
    "     defeat Metal-Salt Monsters.",
    "",
    "Our goal is to strategically command",
    "the three heroes to ward off the",
    "attacks of the Elemental Monsters."
]
rule_text = [
    "1. Colliding with a monster or allowing",
    "  a monster to escape deducts HP equal",
    "  to the monster's remaining health.",
    "",
    "2. If HP=0, then game over.",
    "",
    "3. Defeating monsters grants MP.",
    "",
    "4. Every 10 monsters defeated rewards",
    "  1 magic potion.",
    "",
    "5. Magic potion can freezes monsters",
    "  for 5 seconds.",
    "",
    "6. The monster spawn rate increases",
    "  with the number of defeated monsters.",
    "",
    "7. Remember, only attacks of the right",
    "  attributes can defeat the monsters,",
    "  so choosing the right hero is crucial."
]


class HelpScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = pygame.image.load(resource_path("assets/images/ui/options_bg.jpg"))# 背景图
        self.control_left = pygame.image.load(resource_path("assets/images/ui/control_left.png"))
        self.control_right = pygame.image.load(resource_path("assets/images/ui/control_right.png"))
        self.heros_name = [
            "Base Knight",
            "Acid Hitman",
            "Metal Elf"
        ]
        self.heros_image = [
            pygame.image.load(resource_path("assets/images/ui/hero5.png")),
            pygame.image.load(resource_path("assets/images/ui/hero6.png")),
            pygame.image.load(resource_path("assets/images/ui/hero8.png"))
        ]
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 14)
            self.font_title = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 32)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 28)
            self.font_title = pygame.font.SysFont(None, 32)
        self.font_title.set_underline(True)
        self.title_surface_left = None
        self.title_surface_right = None
        self.line_surfaces_left = []
        self.line_surfaces_right = []

        self.state = 0

        button_width = 50
        button_height = 50
        _x = 20
        _y = 30
        button_back = ImageButton("assets/images/ui/back_arrow.png",
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)
        button_width = 64
        button_height = 46
        _x = 50
        _y = 160
        self.button_rule = TabButton("assets/images/ui/rule1.png", "assets/images/ui/rule2.png",
                                     _x, _y, button_width, button_height,
                                     action=self.show_rule)
        self.button_control = TabButton("assets/images/ui/control1.png", "assets/images/ui/control2.png",
                                        _x + 6, _y + 60, button_width, button_height,
                                        action=self.show_control)
        self.button_role = TabButton("assets/images/ui/role1.png", "assets/images/ui/role2.png",
                                     _x + 12, _y + 120, button_width, button_height,
                                     action=self.show_role)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        # 将按钮添加到精灵组
        self.all_sprites.add(button_back, self.button_rule, self.button_role, self.button_control)

        self.button_rule.set_click_status(True)
        self.show_rule()

    def show_rule(self):
        self.state = 0
        self.title_surface_left = self.font_title.render("Game Goals", True, DARK_RED)
        self.title_surface_right = self.font_title.render("Game Rules", True, DARK_RED)
        self.line_surfaces_left = []
        for line in goal_text:
            line_surface = self.font.render(line, True, BLACK)
            self.line_surfaces_left.append(line_surface)
        self.line_surfaces_right = []
        for line in rule_text:
            line_surface = self.font.render(line, True, BLACK)
            self.line_surfaces_right.append(line_surface)
        self.button_role.set_click_status(False)
        self.button_control.set_click_status(False)

    def show_control(self):
        self.state = 1
        self.title_surface_left = self.font_title.render("Keyboard Control", True, DARK_GREEN)
        self.title_surface_right = self.font_title.render("Mouse Control", True, DARK_GREEN)
        self.button_rule.set_click_status(False)
        self.button_role.set_click_status(False)

    def show_role(self):
        self.state = 2
        self.title_surface_left = self.font_title.render("HEROS", True, DARK_BLUE)
        self.title_surface_right = self.font_title.render("MONSTERS", True, DARK_BLUE)
        self.button_rule.set_click_status(False)
        self.button_control.set_click_status(False)

    def update(self):
        pass

    def render_rule(self, screen):
        _x = 150
        current_y = 160
        if self.line_surfaces_left:
            for line_surface in self.line_surfaces_left:
                screen.blit(line_surface, (_x, current_y))
                current_y += line_surface.get_height() + 5  # 5像素行间距
        current_y = 220
        for img in self.heros_image:
            screen.blit(img, (_x, current_y))
            current_y += 90
        current_y = 160
        if self.line_surfaces_right:
            for line_surface in self.line_surfaces_right:
                line_x = 650
                screen.blit(line_surface, (line_x, current_y))
                current_y += line_surface.get_height() + 4  # 5像素行间距

    def render_control(self, screen):
        _x = 135 + (430 - self.control_left.get_width()) / 2
        _y = 160
        screen.blit(self.control_left, (_x, _y))
        _x = 640 + (430 - self.control_right.get_width()) / 2
        _y = 220
        screen.blit(self.control_right, (_x, _y))

    def render_role(self, screen):
        current_y = 160
        for line_surface in self.line_surfaces_left:
            line_x = 880 - line_surface.get_width()
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + 70

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        if self.title_surface_left:
            _x = 135 + (430 - self.title_surface_left.get_width()) / 2
            _y = 100
            screen.blit(self.title_surface_left, (_x, _y))
        if self.title_surface_right:
            _x = 640 + (430 - self.title_surface_right.get_width()) / 2
            _y = 100
            screen.blit(self.title_surface_right, (_x, _y))
        if self.state == 0:
            self.render_rule(screen)
        elif self.state == 1:
            self.render_control(screen)
        elif self.state == 2:
            self.render_role(screen)
        self.all_sprites.draw(screen)

    def process_input(self, event):
        self.all_sprites.update(event)
