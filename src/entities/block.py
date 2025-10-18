import pygame
import random
from src.config.settings import GRAY, DARK_GRAY, RED, DARK_RED, BLUE, DARK_BLUE, GREEN, DARK_GREEN, BLACK

class ChemicalBlock:
    """化学式方块类"""
    def __init__(self, formula, block_type, x, y):
        self.formula = formula
        self.type = block_type  # 'acid', 'base', 'salt'
        self.x = x
        self.y = y
        self.width = random.randint(50, 200)
        self.height = random.randint(25, 100)
        self.speed = 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = GRAY
        self.border_color = DARK_GRAY

        # 根据类型设置颜色
        if block_type == 'acid':
            self.color = RED
            self.border_color = DARK_RED
        elif block_type == 'base':
            self.color = BLUE
            self.border_color = DARK_BLUE
        else:  # salt
            self.color = GREEN
            self.border_color = DARK_GREEN
    
    def update(self):
        """更新方块位置"""
        self.y += self.speed
        self.rect.y = self.y
        
    def draw(self, screen, font):
        """绘制方块"""
        # 绘制方块背景
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 3)
        
        # 绘制化学式文字
        text = font.render(self.formula, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def is_off_screen(self):
        """检查是否掉出屏幕"""
        return self.y > 600  # SCREEN_HEIGHT from settings