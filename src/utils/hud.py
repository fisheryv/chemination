import pygame
from src.config.settings import GRAY, BLACK, GREEN, YELLOW, RED

class HUD:
    """游戏界面UI类"""
    @staticmethod
    def draw_hud(screen, font, player, game_time, score, difficulty):
        """绘制游戏界面UI"""
        # HP条背景
        hp_bar_bg = pygame.Rect(10, 10, 300, 30)
        pygame.draw.rect(screen, GRAY, hp_bar_bg)
        pygame.draw.rect(screen, BLACK, hp_bar_bg, 2)
        
        # HP条
        hp_percentage = player.hp / player.max_hp
        hp_bar = pygame.Rect(10, 10, int(300 * hp_percentage), 30)
        
        # 根据HP百分比改变颜色
        if hp_percentage > 0.5:
            hp_color = GREEN
        elif hp_percentage > 0.25:
            hp_color = YELLOW
        else:
            hp_color = RED
        pygame.draw.rect(screen, hp_color, hp_bar)
        
        # HP文字
        hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, BLACK)
        hp_text_rect = hp_text.get_rect(center=(160, 25))
        screen.blit(hp_text, hp_text_rect)
        
        # 游戏时间
        time_text = font.render(f"TIME: {game_time:.1f} s", True, BLACK)
        screen.blit(time_text, (800 - 150, 10))  # SCREEN_WIDTH from settings
        
        # 得分
        score_text = font.render(f"SCORE: {score}", True, BLACK)
        screen.blit(score_text, (800 - 150, 40))  # SCREEN_WIDTH from settings
        
        # 角色提示
        role_text = font.render(f"ROLE: {player.role_name}", True, player.color)
        screen.blit(role_text, (10, 50))
        
        # 难度显示
        difficulty_text = font.render(f"DIFFICULTY: {difficulty}", True, BLACK)
        screen.blit(difficulty_text, (10, 80))