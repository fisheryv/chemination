import pygame
from src.config.settings import RED, DARK_RED, BLUE, DARK_BLUE, GREEN, DARK_GREEN, BLACK

class Player:
    """玩家类"""
    def __init__(self, role):
        self.role = role  # 'acid', 'base', 'salt'
        self.hp = 500
        self.max_hp = 500
        self.x = 800 // 2  # SCREEN_WIDTH from settings
        self.y = 600 - 100  # SCREEN_HEIGHT from settings
        self.width = 80
        self.height = 80
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 根据角色设置颜色
        if role == 'acid':
            self.color = RED
            self.role_name = "ACID"
        elif role == 'base':
            self.color = BLUE
            self.role_name = "BASE"
        else:  # salt
            self.color = GREEN
            self.role_name = "SALT"
    
    def move_left(self):
        """向左移动"""
        self.x = max(0, self.x - self.speed)
        self.rect.x = self.x
    
    def move_right(self):
        """向右移动"""
        self.x = min(800 - self.width, self.x + self.speed)  # SCREEN_WIDTH from settings
        self.rect.x = self.x
    
    def draw(self, screen, font):
        """绘制玩家"""
        # 绘制玩家方块
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        
        # 绘制角色名称
        text = font.render(self.role_name, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def take_damage(self, damage):
        """受到伤害"""
        self.hp = max(0, self.hp - damage)
    
    def heal(self, amount):
        """恢复生命值"""
        self.hp = min(self.max_hp, self.hp + amount)