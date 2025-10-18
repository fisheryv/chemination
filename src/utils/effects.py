import pygame
import random

class EffectsManager:
    """特效管理器"""
    def __init__(self):
        self.effects = []  # 存储特效信息
    
    def add_effect(self, x, y, effect_type):
        """添加特效"""
        effect = {
            'x': x,
            'y': y,
            'type': effect_type,  # 'correct' or 'wrong'
            'timer': 30,  # 特效持续帧数
            'particles': []
        }
        
        # 生成粒子
        for i in range(10):
            particle = {
                'dx': random.uniform(-5, 5),
                'dy': random.uniform(-5, 5),
                'size': random.randint(3, 8)
            }
            effect['particles'].append(particle)
        
        self.effects.append(effect)
    
    def update_effects(self):
        """更新特效"""
        for effect in self.effects[:]:
            effect['timer'] -= 1
            if effect['timer'] <= 0:
                self.effects.remove(effect)
            else:
                # 更新粒子位置
                for particle in effect['particles']:
                    particle['dx'] *= 0.95
                    particle['dy'] *= 0.95
    
    def draw_effects(self, screen, correct_color, wrong_color):
        """绘制特效"""
        for effect in self.effects:
            color = correct_color if effect['type'] == 'correct' else wrong_color
            alpha = effect['timer'] * 8
            
            for particle in effect['particles']:
                x = effect['x'] + particle['dx'] * (30 - effect['timer'])
                y = effect['y'] + particle['dy'] * (30 - effect['timer'])
                size = particle['size'] * (effect['timer'] / 30)
                
                if size > 0:
                    pygame.draw.circle(screen, color, (int(x), int(y)), int(size))