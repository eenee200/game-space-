import pygame
import time 
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space+")

# Load and scale background
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT
BG_SCROLL_SPEED = 2

PLAYER_WIDTH, PLAYER_HEIGHT = 30, 70
PLAYER_VEL = 5

STAR_WIDTH = 15
STAR_HEIGHT = 10
STAR_VEL = 3
STAR_POINT = 5

FIRE_RATE = 550  # Milliseconds between shots
POWERUP_DURATION = 3000  # 5 seconds in milliseconds
POWERUP_FIRE_RATE = 150  # Faster fire rate when powered up

POWERUP_WIDTH = 10
POWERUP_HEIGHT = 10
POWERUP_VEL = 3

# Bullet properties
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_VEL = 7
bullets = []

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, powerup_active):
    WIN.blit(BG, (0, bg_y1))
    WIN.blit(BG, (0, bg_y2))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    point_text = FONT.render(f"Score: {round(score)}", 1, "white")
    WIN.blit(point_text, (WIDTH - point_text.get_width() - 10, 10))

    # Draw power-up status
    if powerup_active:
        powerup_text = FONT.render("POWER UP!", 1, "orange")
        WIN.blit(powerup_text, (WIDTH/2 - powerup_text.get_width()/2 - 0, 10))

    pygame.draw.rect(WIN, "green", player)

    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)

    for powerup in powerups:
        pygame.draw.rect(WIN, "orange", powerup)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True
    player = pygame.Rect(WIDTH/2, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    score=0

    start_add_increment = 2000
    start_count = 0

    powerup_add_increment = 2000
    powerup_count = 0

    last_shot_time = 0
    powerup_start_time = 0
    powerup_active = False

    stars = []
    powerups = []
    bullets = []
    hit = False

    bg_y1 = 0
    bg_y2 = -HEIGHT

    while run:
        start_count += clock.tick(60)
        powerup_count += clock.tick(100)
        elapsed_time = time.time() - start_time
        current_time = pygame.time.get_ticks()

        # Check power-up status
        if powerup_active and current_time - powerup_start_time >= POWERUP_DURATION:
            powerup_active = False

        bg_y1 += BG_SCROLL_SPEED
        bg_y2 += BG_SCROLL_SPEED

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        if powerup_count > powerup_add_increment:
            for _ in range(3):
                powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH) 
                powerup = pygame.Rect(powerup_x, -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)
                powerups.append(powerup)

            powerup_add_increment = max(200, powerup_add_increment - 50)
            powerup_count = 0

        if start_count > start_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH) 
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            start_add_increment = max(200, start_add_increment - 50)
            start_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Use appropriate fire rate based on power-up status
        current_fire_rate = POWERUP_FIRE_RATE if powerup_active else FIRE_RATE
        
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and current_time - last_shot_time >= current_fire_rate:
            bullet = pygame.Rect(
                player.x + player.width//2 - BULLET_WIDTH//2,
                player.y,
                BULLET_WIDTH,
                BULLET_HEIGHT
            )
            bullets.append(bullet)
            last_shot_time = current_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL <= WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_s] and player.y + PLAYER_VEL <= HEIGHT - PLAYER_HEIGHT:
            player.y += PLAYER_VEL

        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                bullets.remove(bullet)

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
            for bullet in bullets[:]:
                if star.colliderect(bullet):
                    stars.remove(star)
                    bullets.remove(bullet)
                    score += STAR_POINT
                    break

        for powerup in powerups[:]:
            powerup.y += POWERUP_VEL
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            elif powerup.y + powerup.height >= player.y and powerup.colliderect(player):
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

        draw(player, elapsed_time, score, stars, bullets, powerups, bg_y1, bg_y2, powerup_active)

    pygame.quit()

if __name__ == "__main__":
    main()