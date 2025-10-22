from typing import Optional

import pygame

from src.utils.tools import create_alpha_image, resource_path


class Switcher(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int,
                 width: Optional[int] = None, height: Optional[int] = None,
                 initial_state: bool = False,
                 hover_alpha: int = 220, click_alpha: int = 180, action=None):
        """
        切换按钮类初始化

        参数:
            image_on_path: 开启状态图片路径
            image_off_path: 关闭状态图片路径
            x, y: 按钮位置
            width, height: 按钮尺寸（如果为None则使用图片原始尺寸）
            initial_state: 初始状态 (True为开启，False为关闭)
            hover_alpha: 鼠标悬停时的透明度（0-255）
            click_alpha: 鼠标点击时的透明度（0-255）
            action: 状态改变时执行的回调函数
        """
        super().__init__()

        # 加载并处理图片
        self.image: Optional[pygame.Surface] = None
        self.original_image_on = pygame.image.load(resource_path("assets/images/ui/switcher_on.png")).convert_alpha()
        self.original_image_off = pygame.image.load(resource_path("assets/images/ui/switcher_off.png")).convert_alpha()

        # 调整图片大小（如果指定了尺寸）
        if width and height:
            self.original_image_on = pygame.transform.scale(self.original_image_on, (width, height))
            self.original_image_off = pygame.transform.scale(self.original_image_off, (width, height))

        # 创建不同状态的图像
        self.normal_image_on = self.original_image_on.copy()
        self.hover_image_on = create_alpha_image(self.original_image_on, hover_alpha)
        self.click_image_on = create_alpha_image(self.original_image_on, click_alpha)

        self.normal_image_off = self.original_image_off.copy()
        self.hover_image_off = create_alpha_image(self.original_image_off, hover_alpha)
        self.click_image_off = create_alpha_image(self.original_image_off, click_alpha)

        self.normal_image = None
        self.hover_image = None
        self.click_image = None

        # 按钮状态
        self.is_hovered = False
        self.is_clicked = False
        self.normal_position = (x, y)

        # 设置当前状态和图像
        self.state = initial_state
        self.update_image()

        self.rect = self.image.get_rect(topleft=(x, y))

        # 按钮属性
        self.action = action

    def update_image(self):
        """根据当前状态更新显示的图像"""
        if self.state:  # 开启状态
            self.normal_image = self.normal_image_on
            self.hover_image = self.hover_image_on
            self.click_image = self.click_image_on
        else:  # 关闭状态
            self.normal_image = self.normal_image_off
            self.hover_image = self.hover_image_off
            self.click_image = self.click_image_off

        # 设置当前图像
        if self.is_clicked:
            self.image = self.click_image
        elif self.is_hovered:
            self.image = self.hover_image
        else:
            self.image = self.normal_image

    def update(self, event: pygame.event.Event):
        """更新按钮状态"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 处理鼠标事件
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_clicked = True
                self.rect.topleft = self.normal_position

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked and self.is_hovered:
                # 切换状态
                self.state = not self.state
                if self.action:
                    self.action(self.state)

            self.is_clicked = False
            self.rect.topleft = self.normal_position

        # 更新图像
        self.update_image()

    def get_state(self) -> bool:
        """获取当前状态"""
        return self.state

    def set_state(self, state: bool):
        """设置状态"""
        self.state = state
        self.update_image()
