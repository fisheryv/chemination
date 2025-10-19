import pygame

from src.config.settings import WHITE
from src.utils.tools import create_alpha_image


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=None, height=None, text="",
                 text_color=WHITE, font_size=12, hover_alpha=220, click_alpha=180,
                 click_offset=2, action=None):
        """
        图片按钮类初始化

        参数:
            image_path: 按钮图片路径
            x, y: 按钮位置
            width, height: 按钮尺寸（如果为None则使用图片原始尺寸）
            text: 按钮文本
            text_color: 文本颜色
            font_size: 字体大小
            hover_alpha: 鼠标悬停时的透明度（0-255）
            click_alpha: 鼠标点击时的透明度（0-255）
            click_offset: 点击时按钮下移的像素数
            action: 点击按钮时执行的回调函数
        """
        super().__init__()

        # 加载并处理图片
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # 调整图片大小（如果指定了尺寸）
        if width and height:
            self.original_image = pygame.transform.scale(self.original_image, (width, height))

        # 创建不同状态的图像
        self.normal_image = self.original_image.copy()
        self.hover_image = create_alpha_image(self.original_image, hover_alpha)
        self.click_image = create_alpha_image(self.original_image, click_alpha)

        # 设置当前图像
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # 按钮属性
        self.text = text
        self.text_color = text_color
        self.click_offset = click_offset
        self.action = action

        # 按钮状态
        self.is_hovered = False
        self.is_clicked = False
        self.normal_position = (x, y)
        self.clicked_position = (x + click_offset, y + click_offset)

        # 渲染文本（如果有）
        if self.text:
            # 加载TTF字体文件
            try:
                font = pygame.font.Font("assets/fonts/PixelEmulator.ttf", font_size)
            except FileNotFoundError:
                # 如果字体文件不存在，使用系统默认字体
                font = pygame.font.SysFont(None, font_size)
            self.text_surf = font.render(self.text, True, self.text_color)
            text_rect = self.text_surf.get_rect(center=self.rect.center)
            # 将文本绘制到按钮图像上
            self.normal_image.blit(self.text_surf, text_rect)
            self.hover_image.blit(self.text_surf, text_rect)
            self.click_image.blit(self.text_surf, text_rect)



    def update_image(self):
        """更新按钮图像"""
        if self.is_clicked:
            self.image = self.click_image
        elif self.is_hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image

    def update(self, event):
        """更新按钮状态"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 处理鼠标事件
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.image = self.click_image
                self.rect.topleft = self.clicked_position

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                if self.action:
                    self.action()
            self.is_clicked = False
            self.rect.topleft = self.normal_position

        # 更新图像
        self.update_image()
