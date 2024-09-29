import pygame
import random
import math
from pygame import mixer
import time

# Initialize the pygame
pygame.init()
mixer.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('Images/background.png')
background = pygame.transform.scale(background, (800,600))

# Background Sound
mixer.music.load("Images/game_music.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Images/ufo.png')
pygame.display.set_icon(icon)
image = pygame.image.load('Images/ufo.png')

# Player
playerImg = pygame.image.load('Images/player.png')
playerImg = pygame.transform.scale(playerImg, (70,70))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX=[]
enemyY=[]
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    img = pygame.image.load('Images/alien.png')
    img = pygame.transform.scale(img, (70,70))
    enemyImg.append(img)

    enemyX.append(random.randint(50,700))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(15)

# Bullet
bulletImg = pygame.image.load('Images/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (40,40))
bulletX = 0
bulletY = 480
bulletY_change = 4
bullet_state = "ready"

#Score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

difficulty_multiply= 1
current_difficulty=1
score_num = 0
def select_difficulty():
    global difficulty_multiply
    global enemy_speed
    global current_difficulty
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 64)
        title = font.render('Select Difficulty', True, (255, 255, 255))
        screen.blit(title, (200, 100))

        # Difficulty options
        easy_text = font.render('1. Easy', True, (255, 255, 255))
        medium_text = font.render('2. Medium', True, (255, 255, 255))
        hard_text = font.render('3. Hard', True, (255, 255, 255))

        screen.blit(easy_text, (300, 250))
        screen.blit(medium_text, (300, 350))
        screen.blit(hard_text, (300, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    enemy_speed = 1  # Easy
                    difficulty_multiply = 0.5
                    current_difficulty = difficulty_multiply
                    running = False
                elif event.key == pygame.K_2:
                    enemy_speed = 2  # Medium
                    difficulty_multiply = 1
                    current_difficulty = difficulty_multiply
                    running = False
                elif event.key == pygame.K_3:
                    enemy_speed = 3  # Hard
                    difficulty_multiply = 1.8
                    current_difficulty = difficulty_multiply
                    running = False

        pygame.display.update()


def show_score(x,y):
    score = font.render('Score :' + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

moving_left= False
moving_right=False

over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render('GAME OVER ', True, (255,255,255) )
    screen.blit(over_text,(200,250))

# powerups intro
powerups = []
fast_bullets = pygame.image.load('Images/fast_bullets.png')
fast_bullets = pygame.transform.scale(fast_bullets, (40,40))
freeze = pygame.image.load('Images/freeze.png')
freeze = pygame.transform.scale(freeze, (40,40))
slowed_enemies = pygame.image.load('Images/slowed_enemies.png')
slowed_enemies = pygame.transform.scale(slowed_enemies, (40,40))

# Dictionary to store power-up images
powerup_images = {"fast_bullets": fast_bullets,"freeze": freeze,"slowed_enemies": slowed_enemies,}
active_powerups = {}
powerup_durations = {'fast_bullets': 4,'slowed_enemies': 4,'freeze': 2}
class PowerUp:
    def __init__(self, x, y, effect, duration,images):

        self.x = x
        self.y = y
        self.effect = effect
        self.duration = duration
        self.active = False
        self.speed = 0.5
        self.image = images.get(self.effect)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fall(self):
        self.y += self.speed  # Move the power-up down

    def active(self):
        self.active=True
        self.activation_time = pygame.time.get_ticks()

    def is_active(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.activation_time < self.duration * 1000:
                return True
            else:
                self.deactivate()
        return False

    def deactivate(self):
        self.active = False

    def check_collision(self, playerX, playerY):
        distance = math.sqrt(math.pow(self.x - playerX, 2) + math.pow(self.y - playerY, 2))
        return distance < 30  # Collision radius


# Power-up handling
for powerup in powerups:
    powerup.fall()  # Move the power-up down
    powerup.draw(screen)  # Draw the power-up

    # Check for collision with player
    if powerup.check_collision(playerX, playerY):
        if powerup.effect == 'fast_bullets':
            bulletY_change = 8  # Increase bullet speed
            active_powerups['fast_bullets'] = time.time()  # Store activation time
        elif powerup.effect == 'slowed_enemies':
            difficulty_multiply = 0.5  # Slow down enemies
            active_powerups['slowed_enemies'] = time.time()  # Store activation time
        elif powerup.effect == 'freeze':
            for j in range(num_of_enemies):
                enemyX_change[j] = 0  # Stop enemy movement
            active_powerups['freeze'] = time.time()  # Store activation time

        powerups.remove(powerup)  # Remove power-up after collection

# Game loop
running = True
game_active = True
enemy_speed = 2
select_difficulty()
difficulty_incremented = False


while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key events for movement and shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready" and game_active:
                    bullet_Sound = mixer.Sound('Images/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False



    if moving_left and not moving_right:
        playerX_change = -1.5
    elif moving_right and not moving_left:
        playerX_change = 1.5
    else:
        playerX_change = 0

    # Spaceship Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

    # Increasing difficulty over time
    if score_value > 1 and score_value % 10 == 0 and not difficulty_incremented:
        current_difficulty += 0.5  # Increment difficulty by 1
        difficulty_incremented = True  # Set flag to indicate difficulty has been incremented


    if score_value % 10 != 0:
        difficulty_incremented = False


    # Enemy Movement
    for i in range(num_of_enemies):
        # Checking for Game Over
        if enemyY[i] > 420:
            game_active = False
            playerX_change = 0
            playerX = 370

            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i] * current_difficulty
        if enemyX[i] <= 0 or enemyX[i] >=750:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('Images/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # Power-up drop logic
            if random.random() < 0.3:  # 30% chance to drop a power-up
                powerup_type = random.choice(['fast_bullets', 'freeze', 'slowed_enemies'])
                if powerup_type in ['fast_bullets',"slowed_enemies"]:
                    duration = 4
                else:
                    duration =2
                powerups.append(PowerUp(enemyX[i], enemyY[i], powerup_type, 5, powerup_images))

            enemyX[i] = random.randint(0, 749)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        # Power-up handling
        for powerup in powerups:
            powerup.fall()  # Move the power-up down
            powerup.draw(screen)  # Draw the power-up

            # Check for collision with player
            if powerup.check_collision(playerX, playerY):
                if powerup.effect == 'fast_bullets':
                    bulletY_change = 8  # Increase bullet speed
                    active_powerups['fast_bullets'] = time.time()  # Store activation time
                elif powerup.effect == 'slowed_enemies':
                    difficulty_multiply = current_difficulty  # Store the current difficulty
                    current_difficulty *= 0.5  # Halve the current difficulty
                    active_powerups['slowed_enemies'] = time.time()  # Store activation time
                elif powerup.effect == 'freeze':
                    for j in range(num_of_enemies):
                        enemyX_change[j] = 0  # Stop enemy movement
                    active_powerups['freeze'] = time.time()  # Store activation time

                powerups.remove(powerup)  # Remove power-up after collection

        # Check active power-ups and reset effects if expired
        for effect, activation_time in list(active_powerups.items()):
            current_time = time.time()  # Get current time here
            if current_time - activation_time > powerup_durations[effect]:
                if effect == 'fast_bullets':
                    bulletY_change = 4  # Reset bullet speed
                elif effect == 'slowed_enemies':
                    if current_time - activation_time > powerup_durations['slowed_enemies']:
                        current_difficulty = difficulty_multiply  # Reset to original difficulty
                elif effect == 'freeze':
                    for j in range(num_of_enemies):
                        enemyX_change[j] = 1  # Resume enemy movement
                del active_powerups[effect]  # Remove the effect after duration

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()




