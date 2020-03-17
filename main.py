import pygame
import math
import random

# initialie
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
# player
playerimage = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
playerx_change = 0

enemyimage = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 10

for i in range (num_of_enemy):
    enemyimage.append(pygame.image.load('monster.png'))
    enemyx.append(random.randint(0,736))
    enemyy.append(random.randint(50,100))
    enemyx_change.append(5)
    enemyy_change.append(0)

bulletimage = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 8
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textx = 10
texty = 10

over_text = pygame.font.Font("freesansbold.ttf",70)

def game_over():
    over_text = font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (270, 280))

def show_score(x,y):
    score = font.render("Score = "+ str(score_value), True, (255,255,255))
    screen.blit(score,(x, y))

def player(x, y):
    screen.blit(playerimage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x + 16, y + 10))


def IsCollision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt(math.pow(bulletx - enemyx, 2) + math.pow(bullety - enemyy, 2))
    if distance <= 27:
        return True
    else:
        return False


# game loop
while running:



    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key press right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    for i in range (num_of_enemy):
        if enemyy[i] >440:
            for j in range(num_of_enemy):
                enemyx[j] = 2000
            game_over()
            break


    for i in range (num_of_enemy):
            enemyx[i] += enemyx_change[i]
            if enemyx[i] <= 0:
                enemyy[i] += 40
                enemyx_change[i] = 4
            elif enemyx[i] >= 736:
                enemyy[i] += 60
                enemyx_change[i] = -4

            collision = IsCollision(bulletx, bullety, enemyx[i], enemyy[i])
            if collision == True:
                bullety = 480
                bullet_state = "ready"
                score_value += 1

                enemyx[i] = random.randint(0, 736)
                enemyy[i] = random.randint(50, 150)
            enemy(enemyx[i], enemyy[i], i)

    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change



    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
