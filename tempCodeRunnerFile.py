import math
from pathlib import Path
import random
import pygame
import time 
import random
pygame.font.init()

TITLE_FONT = pygame.font.SysFont("comicsans", 70)
MENU_FONT = pygame.font.SysFont("comicsans", 45)

# Add these new colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

def draw_menu():
    WIN.blit(BG, (0, 0))
    
    # Draw title
    title_text = TITLE_FONT.render("SPACE+", 1, WHITE)
    WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))
    
    # Draw menu options
    start_text = MENU_FONT.render("Press SPACE to Start", 1, YELLOW)
    instructions_text = MENU_FONT.render("Press H for Instructions", 1, YELLOW)
    quit_text = MENU_FONT.render("Press Q to Quit", 1, YELLOW)
    
    WIN.blit(start_text, (WIDTH/2 - start_text.get_width()/2, 300))
    WIN.blit(instructions_text, (WIDTH/2 - instructions_text.get_width()/2, 400))
    WIN.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, 500))
    
    pygame.display.update()

def draw_instructions():
    WIN.blit(BG, (0, 0))
    
    # Draw title
    title_text = TITLE_FONT.render("How to Play", 1, WHITE)
    WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 50))
    
    # Draw instructions
    instructions = [
        "WASD - Move ship",
        "LEFT MOUSE - Shoot",
        "Collect orange powerups for rapid fire",
        "Avoid enemies and survive waves",
        "You have 3 lives",
        "",
        "Press SPACE to return to menu"
    ]
    
    for i, instruction in enumerate(instructions):
        text = MENU_FONT.render(instruction, 1, WHITE)
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, 200 + i * 70))
    
    pygame.display.update()

def menu():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_h:
                    instructions()
                elif event.key == pygame.K_q:
                    return False
    
    return False

def instructions():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        draw_instructions()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space+")

ROOT_DIR = Path(__file__).parent
IMAGE_DIR = ROOT_DIR / "image"



PLAYER_WIDTH, PLAYER_HEIGHT = 50, 70
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load(IMAGE_DIR /"player1.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_MASK = pygame.mask.from_surface(PLAYER_IMAGE)
PLAYER_HP = 3
PLAYER_LIFE = 3
PLAYER_VEL = 5

BG = pygame.transform.scale(pygame.image.load(IMAGE_DIR / "bg.jpg"), (WIDTH, HEIGHT))

# First, add this at the top with other constants:
LIFE_ICON_SIZE = 25  # Size for the life indicator images
LIFE_ICON = pygame.transform.scale(PLAYER_IMAGE, (LIFE_ICON_SIZE, LIFE_ICON_SIZE))
LIFE_SPACING = 35  # Space between life icons


STAR_INITIAL_HP = 2
STAR_WIDTH = 50
STAR_HEIGHT = 50
STAR_VEL = 3
STAR_POINT = 5
STAR_IMAGE = pygame.transform.scale(pygame.image.load(IMAGE_DIR /"star.png"), (STAR_WIDTH, STAR_HEIGHT))
STAR_MASK = pygame.mask.from_surface(STAR_IMAGE)
STAR_DAMAGE = 1

FIRE_RATE = 350
POWERUP_DURATION = 3000
POWERUP_FIRE_RATE = 150

POWERUP_WIDTH = 10
POWERUP_HEIGHT = 10
POWERUP_VEL = 5

BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_VEL = 7
BULLET_DAMAGE = 1

BOSS_WIDTH = 200
BOSS_HEIGHT = 200
BOSS_HP = {
    1: 20,  # Level 1 boss HP
    2: 30,  # Level 2 boss HP
    3: 40   # Level 3 boss HP
}
BOSS_DAMAGE = 2
BOSS_POINT = 50
BOSS_VEL = 2

BOSS_IMAGE = pygame.transform.scale(pygame.image.load(IMAGE_DIR / "star.png"), (BOSS_WIDTH, BOSS_HEIGHT))
BOSS_MASK = pygame.mask.from_surface(BOSS_IMAGE)

FONT = pygame.font.SysFont("comicsans", 30)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random velocity for scattered movement
        self.vel_x = random.randint(-8, 8)
        self.vel_y = random.randint(-10, -2)
        self.lifetime = 30  # Number of frames particle will exist
        self.size = random.randint(2, 4)
        # Create a random color variation of white/gray
        color_value = random.randint(200, 255)
        self.color = (color_value, color_value, color_value)
        self.gravity = 0.5

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity  # Add gravity effect
        self.lifetime -= 1

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.size)

class DamageEffect:
    def __init__(self):
        self.particles = []
    
    def create_particles(self, x, y):
        # Create multiple particles at the damage position
        for _ in range(20):  # Number of particles
            particle = Particle(x, y)
            self.particles.append(particle)
    
    def update(self):
        # Update and remove dead particles
        for particle in self.particles[:]:
            particle.move()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
    
    def draw(self, window):
        for particle in self.particles:
            particle.draw(window)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.life = PLAYER_LIFE
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_HP
        self.mask = PLAYER_MASK
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.damage_effect = DamageEffect()  # Add damage effect system
        self.last_damage_time = 0
        self.invulnerable_time = 2000  # 1 second of invulnerability after taking damage

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.invulnerable_time:
            self.hp -= amount
            self.last_damage_time = current_time
            # Create particles at the player's position
            self.damage_effect.create_particles(
                self.rect.x + self.width // 2,
                self.rect.y + self.height // 2
            )
            return True
        return False

    def collide(self, obj_x, obj_y, obj_mask):
        offset_x = obj_x - self.rect.x
        offset_y = obj_y - self.rect.y
        return self.mask.overlap(obj_mask, (offset_x, offset_y)) is not None
    

class Star:
    def __init__(self, x, y, movement_pattern="linear"):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, STAR_WIDTH, STAR_HEIGHT)
        self.hp = STAR_INITIAL_HP
        self.max_hp = STAR_INITIAL_HP
        self.mask = STAR_MASK
        self.movement_pattern = movement_pattern
        self.angle = 0  # For circular motion
        self.original_x = x  # Store original x position for sine movement
        self.time_created = pygame.time.get_ticks()  # For timing-based movements
        
    def move(self):
        if self.movement_pattern == "linear":
            self.rect.y += STAR_VEL
            
        elif self.movement_pattern == "sine":
            self.rect.y += STAR_VEL
            # Sine wave movement
            self.rect.x = self.original_x + math.sin(self.rect.y / 50) * 100
            
        elif self.movement_pattern == "zigzag":
            self.rect.y += STAR_VEL
            # Zigzag every 40 pixels
            if (self.rect.y // 40) % 2 == 0:
                self.rect.x += 2
            else:
                self.rect.x -= 2
                
        elif self.movement_pattern == "circular":
            self.angle += 0.05
            self.rect.y += STAR_VEL
            self.rect.x = self.original_x + math.cos(self.angle) * 50
            
        elif self.movement_pattern == "chase":
            # Basic player tracking (add player parameter when calling)
            if hasattr(self, 'player'):
                dx = self.player.rect.x - self.rect.x
                dy = self.player.rect.y - self.rect.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist != 0:
                    self.rect.x += (dx / dist) * (STAR_VEL * 0.5)
                    self.rect.y += (dy / dist) * (STAR_VEL * 0.5)
            else:
                self.rect.y += STAR_VEL

    def collide(self, obj_x, obj_y, obj_mask):
        offset_x = obj_x - self.rect.x
        offset_y = obj_y - self.rect.y
        return self.mask.overlap(obj_mask, (offset_x, offset_y)) is not None

# Modified formation functions to include different movement patterns

class Powerup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
def create_single_powerup():
    powerups = []
    powerup = Powerup(WIDTH // 2, -POWERUP_HEIGHT)
    powerups.append(powerup)
    return powerups

def create_triple_powerup():
    powerups = []
    start_x = WIDTH // 4
    for i in range(3):
        x = start_x + (i * WIDTH // 4)
        powerup = Powerup(x, -POWERUP_HEIGHT)
        powerups.append(powerup)
    return powerups

def create_zigzag_powerups():
    powerups = []
    for i in range(6):
        x = WIDTH // 2 + (100 if i % 2 == 0 else -100)
        y = -POWERUP_HEIGHT - (i * 50)
        powerup = Powerup(x, y)
        powerups.append(powerup)
    return powerups

def create_circle_powerups():
    powerups = []
    center_x = WIDTH // 2
    radius = 100
    for i in range(8):
        angle = (i / 8) * 2 * 3.14159  # Convert to radians
        x = center_x + radius * math.cos(angle)
        y = -POWERUP_HEIGHT - radius * (1 - math.sin(angle))
        powerup = Powerup(x, y)
        powerups.append(powerup)
    return powerups

def create_diagonal_powerups():
    powerups = []
    for i in range(5):
        x = (i * WIDTH // 4)
        y = -POWERUP_HEIGHT - (i * 50)  # Diagonal formation
        powerup = Powerup(x, y)
        powerups.append(powerup)
    return powerups

class Wave:
    def __init__(self, pattern_func, powerup_pattern_func=None, delay=2000):
        self.pattern_func = pattern_func
        self.powerup_pattern_func = powerup_pattern_func
        self.delay = delay
        self.spawned = False

def create_v_formation():
    stars = []
    center_x = WIDTH // 2
    start_y = -STAR_HEIGHT
    patterns = ["sine"]
    for i in range(5):
        # Create V pattern with different movement patterns
        left_x = center_x - (i * 40)
        right_x = center_x + (i * 40)
        y = start_y + (i * 40)
        pattern = patterns[i % len(patterns)]
        stars.append(Star(left_x, y, pattern))
        if i > 0:
            stars.append(Star(right_x, y, patterns[(i + 1) % len(patterns)]))
    return stars

def create_line_formation():
    stars = []
    start_x = WIDTH // 4
    patterns = ["sine", "zigzag"]
    for i in range(8):
        x = start_x + (i * 80)
        pattern = patterns[i % len(patterns)]
        stars.append(Star(x, -STAR_HEIGHT, pattern))
    return stars

def create_diamond_formation():
    stars = []
    center_x = WIDTH // 2
    start_y = -STAR_HEIGHT
    patterns = ["sine", "zigzag", "circular", "linear", "chase"]
    positions = [
        (0, 0), (-1, -1), (1, -1),
        (-2, 0), (2, 0),
        (-1, 1), (1, 1),
        (0, 2)
    ]
    for i, (dx, dy) in enumerate(positions):
        x = center_x + (dx * 40)
        y = start_y + (dy * 40)
        pattern = patterns[i % len(patterns)]
        stars.append(Star(x, y, pattern))
    return stars

class Boss:
    def __init__(self, level):
        self.level = level
        self.width = BOSS_WIDTH
        self.height = BOSS_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = -self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hp = BOSS_HP[level]
        self.max_hp = BOSS_HP[level]
        self.mask = BOSS_MASK
        self.pattern_timer = 0
        self.current_pattern = 0
        self.patterns = [
            self.pattern_horizontal,
            self.pattern_circle,
            self.pattern_diagonal
        ]
        self.bullet_cooldown = 1000  # Time between bullet patterns
        self.last_shot = 0
        
    def move(self):
        # Move to initial position if not there yet
        if self.rect.y < 50:
            self.rect.y += BOSS_VEL
            return []
        
        # Execute current pattern and get bullets
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.bullet_cooldown:
            self.last_shot = current_time
            return self.patterns[self.current_pattern]()
        return []
    
    def pattern_horizontal(self):
        bullets = []
        for i in range(5):
            x = self.rect.x + (i * (self.width // 4))
            bullet = pygame.Rect(x, self.rect.y + self.height, BULLET_WIDTH, BULLET_HEIGHT)
            bullets.append(("enemy", bullet, 5))  # (type, bullet_rect, velocity)
        return bullets
    
    def pattern_circle(self):
        bullets = []
        num_bullets = 8
        for i in range(num_bullets):
            angle = (i / num_bullets) * 2 * math.pi
            dx = math.cos(angle) * 5
            dy = math.sin(angle) * 5
            bullet = pygame.Rect(
                self.rect.x + self.width//2,
                self.rect.y + self.height//2,
                BULLET_WIDTH,
                BULLET_HEIGHT
            )
            bullets.append(("enemy", bullet, (dx, dy)))  # (type, bullet_rect, (dx, dy))
        return bullets
    
    def pattern_diagonal(self):
        bullets = []
        for i in range(-2, 3):
            bullet = pygame.Rect(
                self.rect.x + self.width//2,
                self.rect.y + self.height,
                BULLET_WIDTH,
                BULLET_HEIGHT
            )
            bullets.append(("enemy", bullet, (i*2, 5)))  # Diagonal movement
        return bullets
    
    def change_pattern(self):
        self.current_pattern = (self.current_pattern + 1) % len(self.patterns)
    
    def collide(self, obj_x, obj_y, obj_mask):
        offset_x = obj_x - self.rect.x
        offset_y = obj_y - self.rect.y
        return self.mask.overlap(obj_mask, (offset_x, offset_y)) is not None

class Level:
    def __init__(self, number, waves, boss=None):
        self.number = number
        self.waves = waves
        self.boss = boss
        self.current_wave = 0
        self.completed = False
        self.boss_spawned = False

def create_levels():
    levels = []
    
    # Level 1
    level1_waves = [
        Wave(create_v_formation, create_single_powerup),
        Wave(create_line_formation),
        Wave(create_diamond_formation, create_circle_powerups)
    ]
    levels.append(Level(1, level1_waves, Boss(1)))
    
    # Level 2
    level2_waves = [
        Wave(create_line_formation, create_zigzag_powerups),
        Wave(create_diamond_formation),
        Wave(create_v_formation, create_triple_powerup),
        Wave(create_diamond_formation, create_circle_powerups)
    ]
    levels.append(Level(2, level2_waves, Boss(2)))
    
    # Level 3
    level3_waves = [
        Wave(create_diamond_formation, create_diagonal_powerups),
        Wave(create_line_formation),
        Wave(create_v_formation, create_circle_powerups),
        Wave(create_diamond_formation),
        Wave(create_line_formation, create_triple_powerup)
    ]
    levels.append(Level(3, level3_waves, Boss(3)))
    
    return levels


def draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, 
         powerup_active, wave_number, boss, enemy_bullets, level_number):
    WIN.blit(BG, (0, bg_y1))
    WIN.blit(BG, (0, bg_y2))

    player.damage_effect.draw(WIN)

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    point_text = FONT.render(f"Score: {round(score)}", 1, "white")
    WIN.blit(point_text, (WIDTH - point_text.get_width() - 10, 10))

    # wave_text = FONT.render(f"Wave: {wave_number}", 1, "white")
    # WIN.blit(wave_text, (WIDTH//2 - wave_text.get_width()//2, 10))

    # Draw HP
    # health_text = FONT.render(f"HP: {player.hp}", 1, "white")
    # WIN.blit(health_text, (10, 40))

    level_text = FONT.render(f"Level: {level_number}", 1, "white")
    WIN.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 40))
    
    # Draw boss if exists
    if boss:
        WIN.blit(BOSS_IMAGE, (boss.rect.x, boss.rect.y))
        # Draw boss health bar
        health_ratio = boss.hp / boss.max_hp
        health_width = 200
        pygame.draw.rect(WIN, "red", (WIDTH//2 - health_width//2, 20, health_width, 20))
        pygame.draw.rect(WIN, "green", (WIDTH//2 - health_width//2, 20, health_width * health_ratio, 20))
    
    # Draw enemy bullets
    for _, bullet, _ in enemy_bullets:
        pygame.draw.rect(WIN, "red", bullet)

    # Draw life icons instead of text
    for i in range(player.hp):
        WIN.blit(LIFE_ICON, (10 + (i * LIFE_SPACING), 70))

    if powerup_active:
        powerup_text = FONT.render("POWER UP!", 1, "orange")
        WIN.blit(powerup_text, (WIDTH/2 - powerup_text.get_width()/2, 40))

    # Draw player with flashing effect when damaged
    current_time = pygame.time.get_ticks()
    if (current_time - player.last_damage_time) < player.invulnerable_time:
        if (current_time // 100) % 2 == 0:  # Flash every 100ms
            WIN.blit(PLAYER_IMAGE, (player.rect.x, player.rect.y))
    else:
        WIN.blit(PLAYER_IMAGE, (player.rect.x, player.rect.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)

    for powerup in powerups:
        pygame.draw.rect(WIN, "orange", powerup.rect)

    for star in stars:
        WIN.blit(STAR_IMAGE, (star.rect.x, star.rect.y))

    pygame.display.update()

def main():
    run = True
    player = Player(WIDTH/2, HEIGHT-PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    score = 0

    powerup_add_increment = 5000
    powerup_count = 0

    last_shot_time = 0
    powerup_start_time = 0
    powerup_active = False

    levels = create_levels()
    current_level = 0
    boss = None
    enemy_bullets = []

    # waves = [
    #     Wave(create_v_formation, create_circle_powerups),
    #     Wave(create_line_formation, create_zigzag_powerups),
    #     Wave(create_diamond_formation, create_diagonal_powerups),
    #     Wave(create_v_formation),  # Some waves without powerups for variety
    #     Wave(create_line_formation, create_single_powerup),
    #     Wave(create_diamond_formation, create_triple_powerup),
    # ]
    current_wave = 0
    wave_delay = 0
    wave_number = 1

    stars = []
    powerups = []
    bullets = []
    hit = False

    bg_y1 = 0
    bg_y2 = -HEIGHT
    BG_SCROLL_SPEED = 2

    # Create a bullet mask (since it's a simple rectangle)
    bullet_surface = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
    pygame.draw.rect(bullet_surface, "yellow", (0, 0, BULLET_WIDTH, BULLET_HEIGHT))
    BULLET_MASK = pygame.mask.from_surface(bullet_surface)

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        current_time = pygame.time.get_ticks()
        powerup_count += clock.tick(100)
        
        player.damage_effect.update()
        if powerup_active and current_time - powerup_start_time >= POWERUP_DURATION:
            powerup_active = False

        bg_y1 += BG_SCROLL_SPEED
        bg_y2 += BG_SCROLL_SPEED

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        # Wave management
        if len(stars) == 0 and not boss:
            if wave_delay <= 0:
                current_level_obj = levels[current_level]
                if current_level_obj.current_wave < len(current_level_obj.waves):
                    # Spawn normal wave
                    wave = current_level_obj.waves[current_level_obj.current_wave]
                    stars.extend(wave.pattern_func())
                    if wave.powerup_pattern_func:
                        powerups.extend(wave.powerup_pattern_func())
                    current_level_obj.current_wave += 1
                    wave_number += 1
                    wave_delay = wave.delay
                elif not current_level_obj.boss_spawned:
                    # Spawn boss
                    boss = current_level_obj.boss
                    current_level_obj.boss_spawned = True
                else:
                    # Level completed
                    current_level += 1
                    if current_level >= len(levels):
                        # Game completed!
                        victory_text = FONT.render("Congratulations! You've completed the game!", 1, "white")
                        WIN.blit(victory_text, (WIDTH/2 - victory_text.get_width()/2, HEIGHT/2))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        break
            else:
                wave_delay -= clock.get_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        mouse_buttons = pygame.mouse.get_pressed()
        current_fire_rate = POWERUP_FIRE_RATE if powerup_active else FIRE_RATE
        
        if mouse_buttons[0] and current_time - last_shot_time >= current_fire_rate:
            bullet = pygame.Rect(
                player.rect.x + player.rect.width//2 - BULLET_WIDTH//2,
                player.rect.y,
                BULLET_WIDTH,
                BULLET_HEIGHT
            )
            bullets.append(bullet)
            last_shot_time = current_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.rect.x - PLAYER_VEL >= 0:
            player.rect.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.rect.x + PLAYER_VEL <= WIDTH - PLAYER_WIDTH:
            player.rect.x += PLAYER_VEL
        if keys[pygame.K_w] and player.rect.y - PLAYER_VEL >= 0:
            player.rect.y -= PLAYER_VEL
        if keys[pygame.K_s] and player.rect.y + PLAYER_VEL <= HEIGHT - PLAYER_HEIGHT:
            player.rect.y += PLAYER_VEL

        if boss:
            # Move boss and get new bullets
            new_bullets = boss.move()
            enemy_bullets.extend(new_bullets)
            
            # Boss collision with player
            if boss.collide(player.rect.x, player.rect.y, player.mask):
                if player.take_damage(BOSS_DAMAGE):
                    if player.hp <= 0:
                        hit = True
                        break
            
            # Player bullets hitting boss
            for bullet in bullets[:]:
                if boss.collide(bullet.x, bullet.y, BULLET_MASK):
                    bullets.remove(bullet)
                    boss.hp -= BULLET_DAMAGE
                    if boss.hp <= 0:
                        boss = None
                        score += BOSS_POINT
                        break
            
            # Change boss pattern periodically
            current_time = pygame.time.get_ticks()
            if current_time - boss.pattern_timer > 5000:  # Change pattern every 5 seconds
                boss.change_pattern()
                boss.pattern_timer = current_time
        
        # Update enemy bullets
        for bullet_info in enemy_bullets[:]:
            bullet_type, bullet, velocity = bullet_info
            if isinstance(velocity, tuple):
                dx, dy = velocity
                bullet.x += dx
                bullet.y += dy
            else:
                bullet.y += velocity
            
            # Remove off-screen bullets
            if (bullet.y > HEIGHT or bullet.y < 0 or 
                bullet.x > WIDTH or bullet.x < 0):
                enemy_bullets.remove(bullet_info)
                continue
            
            # Check collision with player
            if bullet.colliderect(player.rect):
                enemy_bullets.remove(bullet_info)
                if player.take_damage(1):
                    if player.hp <= 0:
                        hit = True
                        break
        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                bullets.remove(bullet)

        for star in stars[:]:
            # Set player reference for chasing stars
            if star.movement_pattern == "chase":
                star.player = player
            
            # Move star according to its pattern
            star.move()
            
            # Check if star is off screen
            if (star.rect.y > HEIGHT or 
                star.rect.x < -STAR_WIDTH or 
                star.rect.x > WIDTH):
                stars.remove(star)
                continue
            
            # Rest of the collision detection code remains the same
            elif star.collide(player.rect.x, player.rect.y, player.mask):
                if player.take_damage(STAR_DAMAGE):
                    stars.remove(star)
                    if player.hp <= 0:
                            hit = True
                            break
            
            for bullet in bullets[:]:
                if star.collide(bullet.x, bullet.y, BULLET_MASK):
                    bullets.remove(bullet)
                    star.hp -= BULLET_DAMAGE
                    if star.hp <= 0:
                        stars.remove(star)
                        score += STAR_POINT
                    break

        for powerup in powerups[:]:
            powerup.rect.y += POWERUP_VEL
            if powerup.rect.y > HEIGHT:
                powerups.remove(powerup)
            elif powerup.rect.y + powerup.rect.height >= player.rect.y and powerup.rect.colliderect(player.rect):
                powerups.remove(powerup)
                powerup_active = True
                powerup_start_time = current_time
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break

        draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, 
             powerup_active, wave_number, boss, enemy_bullets, levels[current_level].number)

    pass

if __name__ == "__main__":
    pygame.init()
    
    while True:
        show_menu = menu()
        if show_menu:
            main()
        else:
            break
    
    pygame.quit()