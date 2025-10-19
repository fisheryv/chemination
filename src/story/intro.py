import pygame
import time

from src.config.settings import FPS, GOLD

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
                 'to defend their homeland ...']
    },
]


class StoryScene:
    """
    StoryScene 用于绘制游戏启动时的世界观设定个背景故事。
    游戏背景故事以类似连环画的形式展示，分为若干分镜（StoryScene），每个分镜由一张背景图片和一个段文字组成。
    若干分镜组成一个序列，依次播放，分镜之间间隔3s。
    """

    def __init__(self, bg: str, text: list[str]):
        self.bg = "assets/images/story/" + bg
        self.text = text
        # 加载TTF字体文件
        try:
            self.font = pygame.font.Font("assets/fonts/PixelEmulator.ttf", 36)
        except FileNotFoundError:
            # 如果字体文件不存在，使用系统默认字体
            self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        """
        绘制故事场景动画
        1. 背景淡入
        2. 从左自右飞入一个半透明黑色矩形
        3. 矩形宽度与背景图宽度一致，高度为文本高度+20，矩形框垂直居中
        4. 将文本绘制在半透明矩形内
        5. 停留3秒后整个场景淡出
        """
        # 加载背景图像
        background = pygame.image.load(self.bg)
        screen_width, screen_height = screen.get_size()

        # 背景淡入效果
        clock = pygame.time.Clock()
        fade_in_duration = 1.0  # 淡入持续时间(秒)
        fade_in_start_time = time.time()

        while time.time() - fade_in_start_time < fade_in_duration:
            # 计算当前淡入透明度
            fade_progress = (time.time() - fade_in_start_time) / fade_in_duration
            fade_alpha = int(255 * fade_progress)

            # 创建背景淡入遮罩
            background_copy = background.copy()
            fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 255 - fade_alpha))
            background_copy.blit(fade_surface, (0, 0))

            # 绘制淡入中的背景
            screen.blit(background_copy, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)  # 约60 FPS

        # 绘制完全不透明的背景图
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # 等待0.5秒
        # time.sleep(0.5)

        # 渲染多行文本
        line_surfaces = []
        for line in self.text:
            line_surface = self.font.render(line, True, GOLD)  # 白色文本
            line_surfaces.append(line_surface)

        # 计算文本块的总高度
        total_text_height = sum(surface.get_height() for surface in line_surfaces)
        if len(line_surfaces) > 1:
            total_text_height += (len(line_surfaces) - 1) * 5  # 行间距

        # 垂直居中位置计算
        text_block_y = (screen_height - total_text_height) // 2

        # 创建半透明黑色矩形Surface
        rect_height = total_text_height + 20
        rectangle = pygame.Surface((screen_width, rect_height), pygame.SRCALPHA)
        rectangle.fill((0, 0, 0, 180))  # 半透明黑色

        # 飞入动画参数
        rect_y = (screen_height - rect_height) // 2
        rect_x = -screen_width  # 初始位置在屏幕左侧外
        target_x = 0  # 目标位置
        speed = 20  # 飞入速度

        # 飞入动画循环
        while rect_x < target_x:
            # 清除屏幕并重新绘制背景
            screen.blit(background, (0, 0))

            # 更新矩形位置
            rect_x += speed
            if rect_x > target_x:
                rect_x = target_x

            # 绘制矩形
            screen.blit(rectangle, (rect_x, rect_y))

            # 绘制多行文本（水平居中，垂直居中）
            current_y = text_block_y
            for line_surface in line_surfaces:
                line_x = rect_x + (screen_width - line_surface.get_width()) // 2
                screen.blit(line_surface, (line_x, current_y))
                current_y += line_surface.get_height() + 5  # 5像素行间距

            # 更新显示
            pygame.display.flip()
            clock.tick(FPS)  # 60 FPS

        # 矩形完全显示后停留3秒
        start_time = time.time()
        while time.time() - start_time < 3:
            # 持续绘制当前状态
            screen.blit(background, (0, 0))
            screen.blit(rectangle, (0, rect_y))
            # 绘制多行文本（水平居中，垂直居中）
            current_y = text_block_y
            for line_surface in line_surfaces:
                line_x = (screen_width - line_surface.get_width()) // 2
                screen.blit(line_surface, (line_x, current_y))
                current_y += line_surface.get_height() + 5  # 5像素行间距

            pygame.display.flip()
            clock.tick(FPS)

        # 淡出效果
        fade_duration = 1.0  # 淡出持续时间(秒)
        fade_start_time = time.time()
        fade_alpha = 0

        while time.time() - fade_start_time < fade_duration:
            # 计算当前淡出透明度
            fade_progress = (time.time() - fade_start_time) / fade_duration
            fade_alpha = int(255 * fade_progress)

            # 创建淡出遮罩
            fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, fade_alpha))

            # 绘制背景和元素
            screen.blit(background, (0, 0))
            screen.blit(rectangle, (0, rect_y))
            # 绘制多行文本（水平居中，垂直居中）
            current_y = text_block_y
            for line_surface in line_surfaces:
                line_x = (screen_width - line_surface.get_width()) // 2
                screen.blit(line_surface, (line_x, current_y))
                current_y += line_surface.get_height() + 5  # 5像素行间距

            screen.blit(fade_surface, (0, 0))

            # 更新显示
            pygame.display.flip()
            clock.tick(FPS)


def play_story(screen):
    for story in story_book:
        story = StoryScene(story['bg'], story['text'])
        story.draw(screen)
