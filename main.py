import pygame
import constants
from character import Character
from weapon import Weapon
from items import Item
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

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 16)

# Function help scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    image = pygame.transform.scale(image, (w * scale, h * scale))
    return image

# load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

# load potion images
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

# load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

# Load character images
mob_animations = []
mob_types = ["elf", "goblin", "skeleton", "muddy", "tiny_zombie", "big_demon"]

animation_types = ["idle", "run"]
for mob in mob_types:
    # Load images
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# function for text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for displaying game info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))
    #draw_lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    # show score
    draw_text(f" x{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 200, 15)

# DAMAGE TEXT CLASS
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
       pygame.sprite.Sprite.__init__(self)
       self.image = font.render(damage, True, color)
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.counter = 0
    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete text
        self.counter += 1
        if self.counter > 30:
            self.kill()
        

# CREATE PLAYER
player = Character(100,100, 100, mob_animations, 0)

# CREATE ENEMY
enemy = Character(300, 400, 100, mob_animations, 1)

# CREATE PLAYER'S WEAPON
bow = Weapon(bow_image, arrow_image)

# CREATE EMPTY ENEMY LIST
enemy_list = []
enemy_list.append(enemy)

# CREATE SPRITE GROUP
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 500, 0, coin_images)
item_group.add(coin)

score_coin = Item(constants.SCREEN_WIDTH - 200, 20, 0, coin_images)
item_group.add(score_coin)


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

    # draw enemies
    for enemy in enemy_list:
        enemy.update()
        enemy.draw(screen)


    #draw player
    player.update()
    player.draw(screen)

    #draw weapon
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        arrow.draw(screen)
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)

    bow.draw(screen)

    # draw text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # draw items
    item_group.update(player)
    item_group.draw(screen)

    draw_info()
    score_coin.draw(screen)

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
