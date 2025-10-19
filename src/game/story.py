import pygame

from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD, WHITE
from src.entities.button import ImageButton
from src.entities.switcher import Switcher
from src.game.scene import Scene
from src.utils.tools import resource_path

story_book = [
    {
        "bg": "story_bg1.jpg",
        "text": ['Legend has it that there is',
                 'a magical kingdom called Chemminos',
                 'on the distant planet Alchelas.']
    },
    {
        "bg": "story_bg2.jpg",
        "text": ['This country advocates chemistry,',
                 'and almost everyone knows',
                 'some chemical knowledge.',
                 'Chemists have brought great benefits',
                 'to the people and are highly respected.']
    },
    {
        "bg": "story_bg3.jpg",
        "text": ["However, the God of the Void, Xel'Naga, ",
                 'opposes all orders in the world.',
                 'He believes that the people of',
                 'Chemminos have mastered too many',
                 'chemical elements and reactions.']
    },
    {
        "bg": "story_bg4.jpg",
        "text": ["So he launched the Infinite Hypnosis",
                 'and sealed all the chemists in Chemminos',
                 'in the Land of Chaos. ',
                 'He also sent out "Elemental Evil Spirits"',
                 'to attack the Kingdom of Chemminos.']
    },
    {
        "bg": "story_bg5.jpg",
        "text": ["In this moment of crisis,",
                 'Commander Lucas Fisher',
                 'organized the people to resist',
                 'the invasion of the evil spirits.',
                 'They used their chemical knowledge',
                 'to defend their homeland......']
    },
]


class StoryScene(Scene):

    def __init__(self, parent):
        super().__init__(parent)  # 调用父类的构造方法
        self.background = None  # 背景图
        self.story = None
        # 加载TTF字体文件
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 36)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 36)
        self.fade_surface = None
        self.line_surfaces = []
        self.total_text_height = 0
        self.text_block_y = 0
        self.rectangle = None
        self.rect_y = 0
        self.rect_x = 0
        self.step = 0
        self.show_count = 0
        self.fade_progress = 0
        self.status = "FadeIn"
        self.init_story()

    def init_story(self, step=0):
        self.show_count = 0
        self.story = story_book[step]
        bg = resource_path("assets/images/story/" + self.story['bg'])
        # 加载背景图像
        self.background = pygame.image.load(bg)
        self.status = "FadeIn"
        self.line_surfaces = []
        for line in self.story["text"]:
            line_surface = self.font.render(line, True, GOLD)  # 白色文本
            self.line_surfaces.append(line_surface)
        # 计算文本块的总高度
        self.total_text_height = sum(surface.get_height() for surface in self.line_surfaces)
        if len(self.line_surfaces) > 1:
            self.total_text_height += (len(self.line_surfaces) - 1) * 5  # 行间距
            # 垂直居中位置计算
            self.text_block_y = (SCREEN_HEIGHT - self.total_text_height) // 2
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # 创建半透明黑色矩形Surface
        rect_height = self.total_text_height + 20
        self.rectangle = pygame.Surface((SCREEN_WIDTH, rect_height), pygame.SRCALPHA)
        self.rectangle.fill((0, 0, 0, 180))  # 半透明黑色
        self.rect_y = (SCREEN_HEIGHT - rect_height) // 2
        self.rect_x = -SCREEN_WIDTH  # 初始位置在屏幕左侧外

    def update(self):
        if self.status == "FadeIn":
            self.fade_progress += 5
            if self.fade_progress >= 255:
                self.fade_progress = 255
            self.fade_surface.fill((0, 0, 0, 255 - self.fade_progress))
            if self.fade_progress == 255:
                self.status = "Text"
        elif self.status == "Text":
            # 更新矩形位置
            self.rect_x += 20
            if self.rect_x >= 0:
                self.rect_x = 0
                self.status = "Show"
        elif self.status == "Show":
            self.show_count += 1
            if self.show_count >= 180:
                self.status = "FadeOut"
        elif self.status == "FadeOut":
            self.fade_progress -= 5
            if self.fade_progress <= 0:
                self.fade_progress = 0
            self.fade_surface.fill((0, 0, 0, 255 - self.fade_progress))
            if self.fade_progress == 0:
                self.step += 1
                if self.step >= len(story_book):
                    self.parent.main_menu()
                else:
                    self.init_story(self.step)

    def _render_text(self, screen):
        # 绘制矩形
        screen.blit(self.rectangle, (self.rect_x, self.rect_y))

        # 绘制多行文本（水平居中，垂直居中）
        current_y = self.text_block_y
        for line_surface in self.line_surfaces:
            line_x = self.rect_x + (SCREEN_WIDTH - line_surface.get_width()) // 2
            screen.blit(line_surface, (line_x, current_y))
            current_y += line_surface.get_height() + 5  # 5像素行间距

    def render(self, screen):
        """
        绘制故事场景动画
        1. 背景淡入
        2. 从左自右飞入一个半透明黑色矩形
        3. 矩形宽度与背景图宽度一致，高度为文本高度+20，矩形框垂直居中
        4. 将文本绘制在半透明矩形内
        5. 停留3秒后整个场景淡出
        """
        if self.status == "FadeIn":
            screen.blit(self.background, (0, 0))
            screen.blit(self.fade_surface, (0, 0))
        elif self.status == "Text" or self.status == "Show":
            # 绘制背景
            screen.blit(self.background, (0, 0))
            self._render_text(screen)
        elif self.status == "FadeOut":
            screen.blit(self.background, (0, 0))
            self._render_text(screen)
            screen.blit(self.fade_surface, (0, 0))

    def process_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.parent.main_menu()
