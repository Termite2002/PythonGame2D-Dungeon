import string
import pygame
import constants
from character import Character

pygame.init()

# SETUP GAME
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Hell Dungeon")
clock = pygame.time.Clock()

#DEFINE PLAYER MOVEMENT VARIABLES
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Function help scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    image = pygame.transform.scale(image, (w * scale, h * scale))
    return image
animation_list = []
for i in range(4):
    img = pygame.image.load(f"assets/images/characters/elf/idle/{i}.png").convert_alpha()
    img = scale_img(img, constants.SCALE)
    animation_list.append(img)

# CREATE PLAYER
player = Character(100,100, animation_list)


# GAME LOOP
run = True
while run:
    # Control frame rate
    clock.tick(constants.FPS)

    screen.fill(constants.BG)

    #Calculate player movement
    dx = 0
    dy = 0
    if moving_left == True:
        dx = -constants.SPEED
    if moving_right == True:
        dx = constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED

    # Move player
    player.move(dx, dy)

    #draw player
    player.update()
    player.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # TAKE KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # print("left")
                moving_left = True
            if event.key == pygame.K_d:
                # print("right")
                moving_right = True
            if event.key == pygame.K_w:
                # print("up")
                moving_up = True
            if event.key == pygame.K_s:
                # print("down")
                moving_down = True

        # RELEASE KEYBOARD INPUT
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                # print("left")
                moving_left = False
            if event.key == pygame.K_d:
                # print("right")
                moving_right = False
            if event.key == pygame.K_w:
                # print("up")
                moving_up = False
            if event.key == pygame.K_s:
                # print("down")
                moving_down = False
    pygame.display.update()

pygame.quit()
