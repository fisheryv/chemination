import pygame

from src.utils.tools import create_alpha_image


class TabButton(pygame.sprite.Sprite):
    def __init__(self, image_path1, image_path2, x, y, width=None, height=None,
                 hover_alpha=220, action=None):
        """
        图片按钮类初始化

        参数:
            image_path1: 按钮图片路径
            image_path2: 按钮图片路径
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
        self.normal_image = pygame.image.load(image_path1).convert_alpha()
        self.click_image = pygame.image.load(image_path2).convert_alpha()

        # 调整图片大小（如果指定了尺寸）
        if width and height:
            self.normal_image = pygame.transform.scale(self.normal_image, (width, height))
            self.click_image = pygame.transform.scale(self.click_image, (width, height))

        # 创建不同状态的图像
        self.hover_image1 = create_alpha_image(self.normal_image, hover_alpha)
        self.hover_image2 = create_alpha_image(self.click_image, hover_alpha)

        # 设置当前图像
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # 按钮属性
        self.action = action

        # 按钮状态
        self.is_hovered = False
        self.is_clicked = False

    def update_image(self):
        """更新按钮图像"""
        if self.is_clicked:
            if self.is_hovered:
                self.image = self.hover_image2
            else:
                self.image = self.click_image
        else:
            self.image = self.normal_image
            if self.is_hovered:
                self.image = self.hover_image1
            else:
                self.image = self.normal_image

    def set_click_status(self, clicked):
        self.is_clicked = clicked
        self.update_image()

    def update(self, event):
        """更新按钮状态"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 处理鼠标事件
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                if self.action:
                    self.action()

        # 更新图像
        self.update_image()
