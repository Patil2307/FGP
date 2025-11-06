import pygame
import random
import math
import sys

pygame.init()

# Create game window
WIDTH = 1024
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - University Level")

# Load + scale background
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Player
playerImg = pygame.image.load("player.png").convert_alpha()
playerX = WIDTH // 2 - 32
playerY = HEIGHT - 120
playerX_change = 0

# Small Enemies
enemyImg = pygame.image.load("enemy.png").convert_alpha()
enemyImg = pygame.transform.scale(enemyImg, (45, 45))

num_of_enemies = 6
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, WIDTH - 45))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
laserImg = pygame.image.load("laser.png").convert_alpha()
laserImg = pygame.transform.scale(laserImg, (10, 32))
laserX = 0
laserY = playerY
laserY_change = 12
laser_state = "ready"

# Load only laser sound
pygame.mixer.init()
laser_sound = pygame.mixer.Sound("laser.mp3")  # <--- Make sure laser.wav is in same folder

# Score
score_value = 0
font = pygame.font.Font(None, 36)

def show_score():
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    laser_sound.play()  # 🔊 play laser sound
    screen.blit(laserImg, (x + 18, y - 10))

def is_collision(ex, ey, lx, ly):
    distance = math.sqrt((ex - lx)**2 + (ey - ly)**2)
    return distance < 25  # tuned for small enemies

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE and laser_state == "ready":
                laserX = playerX
                fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    playerX = max(0, min(WIDTH - 64, playerX))

    # Enemy movement + Game Over check
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= WIDTH - 45:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # ✅ GAME OVER if enemy touches player
        if enemyY[i] > playerY - 40:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        # Collision check (score)
        if is_collision(enemyX[i], enemyY[i], laserX, laserY):
            laserY = playerY
            laser_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, WIDTH - 45)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i])

    # Laser movement
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    if laserY <= 0:
        laserY = playerY
        laser_state = "ready"

    player(playerX, playerY)
    show_score()
    pygame.display.update()

pygame.quit()
sys.exit()
