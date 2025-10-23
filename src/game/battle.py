import random
import pygame

from src.config.settings import (
    PINK, WHITE, CYAN, SCREEN_WIDTH, BLACK, SCREEN_HEIGHT,
    ENEMY_ESCAPED, ENEMY_KILLED, HERO_ATTACK, RED, GREEN
)
from src.data.chemicals import ENEMIES
from src.entities.bullet import Bullet, BulletType
from src.entities.button import ImageButton
from src.entities.enemy import Enemy
from src.entities.hero import Hero
from src.entities.processbar import ProcessBar
from src.game.scene import Scene
from src.utils.effects import EffectsManager
from src.utils.music import (
    load_background_music, pause_background_music, resume_background_music
)
from src.utils.tools import resource_path


class BattleScene(Scene):
    """Battle scene class"""

    def __init__(self, parent):
        """Initialize battle scene
        
        Args:
            parent: The parent game object that contains this scene.
        """
        super().__init__(parent)

        # Game state
        self.is_running = True
        self.is_frozen = False

        # Load resources
        self._load_resources()

        # Initialize game data
        self._init_game_data()

        # Create player and sprite groups
        self._init_sprites()

        # Initialize effects manager
        self.effects_manager = EffectsManager()

        # Initialize pause screen
        self._init_pause_screen()

        # Timers
        self.enemy_spawn_timer = 0
        self.frozen_timer = 0

        # Load background music
        load_background_music("battle_bgm.mp3")

    def _load_resources(self):
        """Load game resources"""
        try:
            self.background = pygame.image.load(resource_path("assets/images/battle/battle_bg1.jpg"))
        except pygame.error:
            # If unable to load background image, create a solid color background as substitute
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 100))

        try:
            self.rip = pygame.image.load(resource_path("assets/images/ui/rip.png"))
            self.rip = pygame.transform.scale(self.rip, (30, 30))
        except pygame.error:
            # Create simple substitute graphics
            self.rip = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.rip.fill((255, 0, 0, 128))

        try:
            self.boom = pygame.image.load(resource_path("assets/images/ui/boom.png"))
            self.boom = pygame.transform.scale(self.boom, (30, 30))
        except pygame.error:
            # Create simple substitute graphics
            self.boom = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.boom.fill((255, 255, 0, 128))

        # Pause button
        self.pause_button = ImageButton(
            resource_path("assets/images/ui/pause.png"),
            SCREEN_WIDTH - 120, 10, 82, 30,
            action=self.pause_game
        )

        # Load font
        try:
            self.font = pygame.font.Font(resource_path("assets/fonts/PixelEmulator.ttf"), 20)
        except (FileNotFoundError, pygame.error):
            # If font file does not exist, use system default font
            self.font = pygame.font.SysFont(None, 24)

    def _init_game_data(self):
        """Initialize game data"""
        # Player attributes
        self.hp = 100
        self.mp = 0

        # Progress bars
        self.hp_bar = ProcessBar(20, 10, 300, 30, PINK, WHITE, "hp.png")
        self.hp_bar.set_progress(self.hp)
        self.mp_bar = ProcessBar(360, 10, 300, 30, CYAN, WHITE, "mp.png")
        self.mp_bar.set_progress(self.mp)

        # Top info bar
        self.rectangle = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
        self.rectangle.fill((255, 255, 255, 128))

        # Kill count
        self.kill_count = 0
        self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)

        # Skill points
        self.boom_count = 3
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)

    def _init_sprites(self):
        """Initialize sprite groups"""
        # Create player
        self.player = Hero()

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group(self.pause_button)

    def _init_pause_screen(self):
        """Initialize pause screen"""
        # Pause overlay
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))

        # Pause panel
        try:
            self.pause_screen = pygame.image.load(resource_path("assets/images/ui/board.png"))
        except pygame.error:
            # Create simple substitute graphics
            self.pause_screen = pygame.Surface((504, 369), pygame.SRCALPHA)
            self.pause_screen.fill((100, 100, 100, 200))

        # Pause screen buttons
        self.start_button = ImageButton(
            resource_path("assets/images/ui/start.png"),
            (SCREEN_WIDTH - 127) // 2, SCREEN_HEIGHT // 2 - 20, 127, 50,
            action=self.resume_game
        )
        self.stop_button = ImageButton(
            resource_path("assets/images/ui/stop.png"),
            (SCREEN_WIDTH - 127) // 2, SCREEN_HEIGHT // 2 + 50, 127, 50,
            action=self.parent.main_menu
        )
        self.overlay_sprites = pygame.sprite.Group(self.start_button, self.stop_button)

    def pause_game(self):
        """Pause game"""
        self.is_running = False
        pause_background_music()

    def resume_game(self):
        """Resume game"""
        self.is_running = True
        resume_background_music()

    def spawn_enemy(self):
        """Spawn enemy"""
        enemy_name = random.choice(list(ENEMIES.keys()))
        enemy = Enemy(enemy_name, ENEMIES[enemy_name])
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)
        self.enemy_spawn_timer = 0

    def freeze_enemy(self):
        """Freeze all enemies"""
        self.is_frozen = True
        self.frozen_timer = 0
        self.boom_count -= 1
        self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)
        for e in self.enemies:
            e.freeze()

    def unfreeze_enemy(self):
        """Unfreeze all enemies"""
        self.is_frozen = False
        self.frozen_timer = 0
        for e in self.enemies:
            e.unfreeze()

    def shoot(self, x: int, y: int, direction: int, bullet_type: BulletType):
        """
        Fire bullet
        
        Args:
            x:           Bullet initial x coordinate
            y:           Bullet initial y coordinate
            direction:   Bullet direction
            bullet_type: Bullet type
        """
        bullet = Bullet(x, y, direction, bullet_type)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self):
        """Update game state"""
        # Do not update when paused
        if not self.is_running:
            return

        # Spawn enemies
        if not self.is_frozen:
            self.enemy_spawn_timer += 1
            # Enemy spawn speed increases with kill count (minimum interval 120 frames)
            spawn_interval = max(300 - self.kill_count, 120)
            if self.enemy_spawn_timer >= spawn_interval:
                self.spawn_enemy()
        else:
            # Update freeze timer
            self.frozen_timer += 1
            if self.frozen_timer >= 300:  # Unfreeze after 300 frames
                self.unfreeze_enemy()

        # Update all sprites
        self.all_sprites.update()

        # Detect collision between player and enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for hit in hits:
            self.hp -= hit.health
            if self.hp <= 0:
                self.parent.game_over()
            self.hp_bar.set_progress(self.hp)
            self.effects_manager.add_effect(hit.rect.x, hit.rect.centery, RED)
            # Delete enemy
            hit.kill()

        # Collision detection: bullets and enemies
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(bullet.bullet_type)

        # Update effects
        self.effects_manager.update_effects()

    def render(self, screen: pygame.Surface):
        """Render the battle scene to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        # Draw background
        screen.blit(self.background, (0, 0))

        # Draw game data bar
        screen.blit(self.rectangle, (0, 0))
        self.hp_bar.draw(screen)
        self.mp_bar.draw(screen)

        # Draw skill icon and count
        x_pos = self.mp_bar.x + self.mp_bar.width + 10
        screen.blit(self.boom, (x_pos, 10))
        x_pos += self.boom.get_width()
        screen.blit(self.boom_count_text, (x_pos, 12))

        # Draw kill count
        x_pos += 60
        screen.blit(self.rip, (x_pos, 10))
        x_pos += self.rip.get_width() + 10
        screen.blit(self.kill_count_text, (x_pos, 12))

        # Draw all sprites
        self.ui_sprites.draw(screen)
        self.all_sprites.draw(screen)
        for e in self.enemies:
            e.draw_hp(screen)

        # Draw effects
        self.effects_manager.draw_effects(screen)

        # Draw pause screen
        if not self.is_running:
            screen.blit(self.overlay, (0, 0))
            screen.blit(self.pause_screen, ((SCREEN_WIDTH - 504) / 2, (SCREEN_HEIGHT - 369) / 2))
            self.overlay_sprites.draw(screen)

    def process_input(self, event: pygame.event.Event):
        """Process user input events.

        Args:
            event: The pygame event to process.
        """
        # Handle pause screen events
        if not self.is_running:
            self.overlay_sprites.update(event)
            return

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.shoot()

        elif event.type == pygame.KEYUP:
            # Character switching
            if event.key == pygame.K_LEFT:
                hero_type = (self.player.hero_type - 1) % 3
                self.player.change_hero(hero_type)
            elif event.key == pygame.K_RIGHT:
                hero_type = (self.player.hero_type + 1) % 3
                self.player.change_hero(hero_type)
            # Skill release
            elif event.key == pygame.K_x:
                if not self.is_frozen and self.boom_count > 0:
                    self.freeze_enemy()

        # Handle mouse events
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click to shoot
                self.player.shoot()
            elif event.button == 3:  # Right click to switch character
                hero_type = (self.player.hero_type + 1) % 3
                self.player.change_hero(hero_type)

        # Handle custom events
        elif event.type == HERO_ATTACK:  # Player attack
            self.shoot(**event.dict)
        elif event.type == ENEMY_ESCAPED:  # Enemy escape
            enemy = event.dict.get('enemy', None)
            damage = event.dict.get('damage', 0)
            if enemy:
                self.hp -= damage
                self.hp_bar.set_progress(self.hp)
                self.effects_manager.add_effect(0, enemy.rect.centery, RED)
                if self.hp <= 0:
                    self.parent.game_over()

        elif event.type == ENEMY_KILLED:  # Enemy killed
            enemy = event.dict.get('enemy', None)
            if enemy:
                self.kill_count += 1
                self.mp += 10
                self.mp_bar.set_progress(self.mp)
                self.kill_count_text = self.font.render("Kill Count: " + str(self.kill_count), True, BLACK)
                self.effects_manager.add_effect(enemy.rect.x, enemy.rect.centery, GREEN)

                # Gain one skill point for every 10 enemies killed
                if self.kill_count % 10 == 0:
                    self.mp = 0
                    self.mp_bar.set_progress(self.mp)
                    self.boom_count += 1
                    self.boom_count_text = self.font.render("x" + str(self.boom_count), True, BLACK)

        # Update UI sprites
        self.ui_sprites.update(event)
