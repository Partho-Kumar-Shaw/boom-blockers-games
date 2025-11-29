#!/usr/bin/env python3
# client/game.py
"""
Pygame Ship Shooter — runs standalone.
If client/assets contains images/sounds with the expected names they will be used.
Otherwise the game draws simple placeholders so it still runs.
"""

import os
import sys
import random
import time
import pygame

# --- AUTO-DETECT ASSETS FOLDER ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_asset_path(file):
    return os.path.join(ASSETS_DIR, file)

def safe_load_image(name):
    path = load_asset_path(name)
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        return None

def safe_load_sound(name):
    path = load_asset_path(name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ship Shooter - Easy Mode + Powerups")

# Try to load assets
SHIP_IMG = safe_load_image("ship.png")
ENEMY_IMG = safe_load_image("enemy.png")
BOSS_IMG = safe_load_image("boss.png")
BULLET_IMG = safe_load_image("bullet.png")
BG_IMG = safe_load_image("background.png")
LIFE_IMG = safe_load_image("life.png")

# Sounds (optional)
try:
    pygame.mixer.init()
except Exception:
    pass

shoot_sound = safe_load_sound("shoot.wav")
explosion_sound = safe_load_sound("explosion.wav")

music_path = load_asset_path("music.wav")
if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

# If images aren't available, create simple placeholders
if SHIP_IMG is None:
    SHIP_IMG = pygame.Surface((60, 48), pygame.SRCALPHA)
    pygame.draw.polygon(SHIP_IMG, (30, 144, 255), [(0,48),(30,0),(60,48)])

if ENEMY_IMG is None:
    ENEMY_IMG = pygame.Surface((40, 28), pygame.SRCALPHA)
    pygame.draw.rect(ENEMY_IMG, (220,20,60), ENEMY_IMG.get_rect(), border_radius=6)

if BOSS_IMG is None:
    BOSS_IMG = pygame.Surface((140, 80), pygame.SRCALPHA)
    pygame.draw.rect(BOSS_IMG, (128,0,128), BOSS_IMG.get_rect(), border_radius=10)

if BULLET_IMG is None:
    BULLET_IMG = pygame.Surface((6, 12), pygame.SRCALPHA)
    pygame.draw.rect(BULLET_IMG, (255,215,0), BULLET_IMG.get_rect())

if BG_IMG is None:
    BG_IMG = pygame.Surface((WIDTH, HEIGHT))
    BG_IMG.fill((12, 12, 30))
    for _ in range(80):
        pygame.draw.circle(BG_IMG, (255,255,255), (random.randint(0,WIDTH), random.randint(0,HEIGHT)), random.choice([1,1,2]))

if LIFE_IMG is None:
    LIFE_IMG = pygame.Surface((30, 24), pygame.SRCALPHA)
    pygame.draw.circle(LIFE_IMG, (255,0,0), (15,12), 10)

# Game variables
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 8
BASE_ENEMY_SPEED = 2
BASE_BOSS_SPEED = 2
BASE_BOSS_HEALTH = 20
FIRE_DELAY = 300

font = pygame.font.Font(None, 36)

# Powerup Types
POWERUP_TYPES = ["rapid", "shield", "double"]

class Player:
    def __init__(self):
        self.image = SHIP_IMG
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-60))
        self.lives = 3
        self.score = 0
        self.invincible = False
        self.double_bullets = False

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def draw(self):
        screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y, speed):
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Boss:
    def __init__(self, health, speed):
        self.image = BOSS_IMG
        self.rect = self.image.get_rect(center=(WIDTH//2, 100))
        self.health = health
        self.direction = 1
        self.speed = speed

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def draw(self):
        screen.blit(self.image, self.rect)

class PowerUp:
    def __init__(self, x, y, kind):
        self.kind = kind
        self.color = (0, 255, 0) if kind == "shield" else (255, 255, 0) if kind == "rapid" else (0, 200, 255)
        self.rect = pygame.Rect(x, y, 25, 25)

    def update(self):
        self.rect.y += 2

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.wave = 1
        self.boss = None
        self.enemy_speed = BASE_ENEMY_SPEED
        self.boss_health = BASE_BOSS_HEALTH
        self.boss_speed = BASE_BOSS_SPEED
        self.running = True
        self.rapid_fire = False
        self.rapid_end_time = 0
        self.shield_end_time = 0
        self.double_end_time = 0

    def spawn_wave(self):
        enemies_to_spawn = min(5 + self.wave * 2, 25)
        for i in range(enemies_to_spawn):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(-300, -50)
            self.enemies.append(Enemy(x, y, self.enemy_speed))

    def spawn_powerup(self, x, y):
        if random.random() < 0.25:
            kind = random.choice(POWERUP_TYPES)
            self.powerups.append(PowerUp(x, y, kind))

    def activate_powerup(self, kind):
        if kind == "rapid":
            self.rapid_fire = True
            self.rapid_end_time = time.time() + 5
        elif kind == "shield":
            self.player.invincible = True
            self.shield_end_time = time.time() + 5
        elif kind == "double":
            self.player.double_bullets = True
            self.double_end_time = time.time() + 5

    def update_powerups(self):
        if self.rapid_fire and time.time() > self.rapid_end_time:
            self.rapid_fire = False
        if self.player.invincible and time.time() > self.shield_end_time:
            self.player.invincible = False
        if self.player.double_bullets and time.time() > self.double_end_time:
            self.player.double_bullets = False

    def update(self):
        self.update_powerups()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.rect.top > HEIGHT:
                self.enemies.remove(enemy)
                if not self.player.invincible:
                    self.player.lives -= 1
            for bullet in self.bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.spawn_powerup(enemy.rect.x, enemy.rect.y)
                        self.player.score += 10
                        if explosion_sound:
                            try:
                                explosion_sound.play()
                            except Exception:
                                pass
                    break

        for power in self.powerups[:]:
            power.update()
            if power.rect.top > HEIGHT:
                self.powerups.remove(power)
            if power.rect.colliderect(self.player.rect):
                self.activate_powerup(power.kind)
                self.powerups.remove(power)

        if not self.enemies and not self.boss:
            if self.wave % 3 == 0:
                self.boss = Boss(self.boss_health, self.boss_speed)
            else:
                self.wave += 1
                self.spawn_wave()

        if self.boss:
            self.boss.update()
            for bullet in self.bullets[:]:
                if bullet.rect.colliderect(self.boss.rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.boss.health -= 1
                    if explosion_sound:
                        try:
                            explosion_sound.play()
                        except Exception:
                            pass
                    if self.boss.health <= 0:
                        self.boss = None
                        self.wave += 1
                        self.spawn_wave()
                        self.player.score += 100

    def draw(self):
        screen.blit(BG_IMG, (0, 0))
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()
        for enemy in self.enemies:
            enemy.draw()
        if self.boss:
            self.boss.draw()
        for power in self.powerups:
            power.draw()

        for i in range(self.player.lives):
            screen.blit(LIFE_IMG, (10 + i*40, 10))
        score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH-150, 10))

game = Game()
game.spawn_wave()

def restart_game():
    global game
    game = Game()
    game.spawn_wave()

clock = pygame.time.Clock()
last_shot_time = 0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        game.player.move(-PLAYER_SPEED)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        game.player.move(PLAYER_SPEED)

    fire_delay = 100 if game.rapid_fire else FIRE_DELAY
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time >= fire_delay:
            if game.player.double_bullets:
                game.bullets.append(Bullet(game.player.rect.centerx - 10, game.player.rect.top))
                game.bullets.append(Bullet(game.player.rect.centerx + 10, game.player.rect.top))
            else:
                game.bullets.append(Bullet(game.player.rect.centerx, game.player.rect.top))
            if shoot_sound:
                try:
                    shoot_sound.play()
                except Exception:
                    pass
            last_shot_time = current_time

    game.update()
    game.draw()

    if game.player.lives <= 0:
        game_over_text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2))

    pygame.display.flip()
