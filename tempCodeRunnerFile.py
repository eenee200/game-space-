import math
from pathlib import Path
import pygame
import time 
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
PLAYER_VEL = 5

BG = pygame.transform.scale(pygame.image.load(IMAGE_DIR / "bg.jpg"), (WIDTH, HEIGHT))


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
POWERUP_VEL = 7

BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_VEL = 7
BULLET_DAMAGE = 1

FONT = pygame.font.SysFont("comicsans", 30)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_HP
        self.mask = PLAYER_MASK
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

    def collide(self, obj_x, obj_y, obj_mask):
        offset_x = obj_x - self.rect.x
        offset_y = obj_y - self.rect.y
        return self.mask.overlap(obj_mask, (offset_x, offset_y)) is not None
    

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, STAR_WIDTH, STAR_HEIGHT)
        self.hp = STAR_INITIAL_HP
        self.max_hp = STAR_INITIAL_HP
        self.mask = STAR_MASK

    def collide(self, obj_x, obj_y, obj_mask):
        offset_x = obj_x - self.rect.x
        offset_y = obj_y - self.rect.y
        return self.mask.overlap(obj_mask, (offset_x, offset_y)) is not None
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
    for i in range(5):
        # Create V pattern
        left_x = center_x - (i * 40)
        right_x = center_x + (i * 40)
        y = start_y + (i * 40)
        stars.append(Star(left_x, y))
        if i > 0:  # Don't create duplicate star at the point of the V
            stars.append(Star(right_x, y))
    return stars

def create_line_formation():
    stars = []
    start_x = WIDTH // 4
    for i in range(8):
        x = start_x + (i * 80)
        stars.append(Star(x, -STAR_HEIGHT))
    return stars

def create_diamond_formation():
    stars = []
    center_x = WIDTH // 2
    start_y = -STAR_HEIGHT
    # Create diamond pattern
    positions = [
        (0, 0), (-1, -1), (1, -1),
        (-2, 0), (2, 0),
        (-1, 1), (1, 1),
        (0, 2)
    ]
    for dx, dy in positions:
        x = center_x + (dx * 40)
        y = start_y + (dy * 40)
        stars.append(Star(x, y))
    return stars

def draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, powerup_active, wave_number):
    WIN.blit(BG, (0, bg_y1))
    WIN.blit(BG, (0, bg_y2))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    point_text = FONT.render(f"Score: {round(score)}", 1, "white")
    WIN.blit(point_text, (WIDTH - point_text.get_width() - 10, 10))

    wave_text = FONT.render(f"Wave: {wave_number}", 1, "white")
    WIN.blit(wave_text, (WIDTH//2 - wave_text.get_width()//2, 10))

    # Add health display
    health_text = FONT.render(f"HP: {player.hp}", 1, "white")
    WIN.blit(health_text, (10, 40))

    if powerup_active:
        powerup_text = FONT.render("POWER UP!", 1, "orange")
        WIN.blit(powerup_text, (WIDTH/2 - powerup_text.get_width()/2, 40))

    WIN.blit(PLAYER_IMAGE, (player.rect.x, player.rect.y))  # Changed from player.x to player.rect.x

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

    waves = [
        Wave(create_v_formation, create_single_powerup),
        Wave(create_line_formation, create_zigzag_powerups),
        Wave(create_diamond_formation, create_diagonal_powerups),
        Wave(create_v_formation),  # Some waves without powerups for variety
        Wave(create_line_formation, create_single_powerup),
        Wave(create_diamond_formation, create_triple_powerup),
    ]
    current_wave = 0
    wave_delay = 0

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

        if powerup_active and current_time - powerup_start_time >= POWERUP_DURATION:
            powerup_active = False

        bg_y1 += BG_SCROLL_SPEED
        bg_y2 += BG_SCROLL_SPEED

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        # Wave management
        if len(stars) == 0:
            if wave_delay <= 0:
                if current_wave < len(waves):
                    # Spawn stars
                    new_stars = waves[current_wave].pattern_func()
                    stars.extend(new_stars)
                    
                    # Spawn powerups if wave has powerup pattern
                    if waves[current_wave].powerup_pattern_func:
                        new_powerups = waves[current_wave].powerup_pattern_func()
                        powerups.extend(new_powerups)
                    
                    current_wave += 1
                    wave_delay = waves[current_wave-1].delay
                else:
                    # Reset to first wave when all waves are complete
                    current_wave = 0
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

        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                bullets.remove(bullet)

        for star in stars[:]:
            star.rect.y += STAR_VEL
            if star.rect.y > HEIGHT:
                stars.remove(star)
            elif star.collide(player.rect.x, player.rect.y, player.mask):
                stars.remove(star)
                player.hp -= STAR_DAMAGE
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
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, powerup_active, current_wave + 1)  # Changed from player.rect to player

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