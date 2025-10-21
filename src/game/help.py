import pygame

from src.config.settings import DARK_RED, BLACK, DARK_GREEN, DARK_BLUE, DARK_GRAY
from src.data.chemicals import ENEMIES_SPIRIT, ENEMIES
from src.entities.button import ImageButton
from src.entities.tab import TabButton
from src.game.scene import Scene
from src.utils.tools import resource_path, load_sprite_sheet

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
        self.background = pygame.image.load(resource_path("assets/images/ui/options_bg.jpg"))  # 背景图
        self.control_left = pygame.image.load(resource_path("assets/images/ui/control_left.png"))
        self.control_right = pygame.image.load(resource_path("assets/images/ui/control_right.png"))
        self.heart = pygame.image.load(resource_path("assets/images/ui/heart3.png"))
        self.heros_name = [
            "Base Knight",
            "Acid Hitman",
            "Metal Elf"
        ]
        self.heros_image = [pygame.image.load(resource_path(f"assets/images/ui/hero{i + 1}.png")) for i in range(3)]
        # 从精灵图加载所有怪物图像，分类为酸1、酸2、碱1、碱2、盐
        self.animations = load_sprite_sheet("assets/images/enemy/monsters.png",
                                            5, 4, directions=("a1", "a2", "b1", "b2", "s"), scale=1)
        # 将盐和碱的最后一帧添加到金属帧列表中
        metal_frame = [
            self.animations["b1"].pop(),
            self.animations["b2"].pop(),
            self.animations["s"].pop()
        ]
        self.animations["m"] = metal_frame
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 14)
            self.font_title = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 32)
            self.font_subtitle = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 20)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 14)
            self.font_title = pygame.font.SysFont(None, 32)
            self.font_subtitle = pygame.font.SysFont(None, 20)
        self.font_name = pygame.font.SysFont(None, 20)
        self.font_title.set_underline(True)
        self.font_subtitle.set_underline(True)
        self.title_surface_left = None
        self.title_surface_right = None
        self.line_surfaces_left = []
        self.line_surfaces_right = []

        self.state = 0

        button_width, button_height = 50, 50
        _x, _y = 20, 30
        button_back = ImageButton(resource_path("assets/images/ui/back_arrow.png"),
                                  _x, _y, button_width, button_height,
                                  action=self.parent.main_menu)
        button_width, button_height = 64, 46
        _x, _y = 50, 160
        self.button_rule = TabButton(resource_path("assets/images/ui/rule1.png"),
                                     resource_path("assets/images/ui/rule2.png"),
                                     _x, _y, button_width, button_height,
                                     action=self.show_rule)
        self.button_control = TabButton(resource_path("assets/images/ui/control1.png"),
                                        resource_path("assets/images/ui/control2.png"),
                                        _x + 6, _y + 60, button_width, button_height,
                                        action=self.show_control)
        self.button_role = TabButton(resource_path("assets/images/ui/role1.png"),
                                     resource_path("assets/images/ui/role2.png"),
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
        self.title_surface_left = []
        self.title_surface_right = []
        self.button_rule.set_click_status(False)
        self.button_control.set_click_status(False)

    def update(self):
        pass

    def render_rule(self, screen):
        _x, _y = 150, 160
        if self.line_surfaces_left:
            for line_surface in self.line_surfaces_left:
                screen.blit(line_surface, (_x, _y))
                _y += line_surface.get_height() + 5  # 5像素行间距
        _y = 220
        for img in self.heros_image:
            screen.blit(img, (_x, _y))
            _y += 90
        _x, _y = 650, 160
        if self.line_surfaces_right:
            for line_surface in self.line_surfaces_right:
                screen.blit(line_surface, (_x, _y))
                _y += line_surface.get_height() + 4  # 5像素行间距

    def render_control(self, screen):
        _x, _y = 150 + (400 - self.control_left.get_width()) / 2, 160
        screen.blit(self.control_left, (_x, _y))
        _x, _y = 650 + (400 - self.control_right.get_width()) / 2, 220
        screen.blit(self.control_right, (_x, _y))

    def _render_monsters(self, screen, x, y, frames, names):
        x += 100 * (4 - len(frames)) / 2
        for i, f in enumerate(frames):
            screen.blit(f, (x, y))
            _name = names[i]
            _hp = ENEMIES[_name]["hp"]
            _name_frame = self.font_name.render(_name, True, BLACK)
            screen.blit(_name_frame, (x + (80 - _name_frame.get_width()) / 2, y + 80))
            _x = x + (80 - self.heart.get_width() * _hp) / 2
            for k in range(_hp):
                screen.blit(self.heart, (_x + k * self.heart.get_width(), y - self.heart.get_height()))
            x += 100

    def _render_monster_group(self, screen, x, y, title, color, group_names):
        _title = self.font_subtitle.render(title, True, color)
        _x, _y = x + (400 - _title.get_width()) / 2, y
        screen.blit(_title, (_x, _y))
        _x, _y = x + 10, y + 50
        for t in group_names:
            _names = ENEMIES_SPIRIT[t]
            _frames = self.animations[t]
            self._render_monsters(screen, _x, _y, _frames, _names)
            _x, _y = x + 10, _y + 130

    def render_role(self, screen):
        # render acid monsters
        self._render_monster_group(screen, 150, 100, "Acid Monsters", DARK_RED, ["a1", "a2"])

        # render salt monsters
        self._render_monster_group(screen, 150, 420, "Salt Monsters", DARK_GREEN, ["s"])

        # render acid monsters
        self._render_monster_group(screen, 650, 100, "Base Monsters", DARK_BLUE, ["b1", "b2"])

        # render metal monsters
        self._render_monster_group(screen, 650, 420, "Metal Monsters", DARK_GRAY, ["m"])

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        if self.title_surface_left:
            _x = 150 + (400 - self.title_surface_left.get_width()) / 2
            _y = 100
            screen.blit(self.title_surface_left, (_x, _y))
        if self.title_surface_right:
            _x = 650 + (400 - self.title_surface_right.get_width()) / 2
            _y = 100
            screen.blit(self.title_surface_right, (_x, _y))
        if self.state == 0:
            self.render_rule(screen)
        elif self.state == 1:
            self.render_control(screen)
        elif self.state == 2:
            self.render_role(screen)
        self.all_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        self.all_sprites.update(event)
