
import pygame
from pygame import mixer
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button

mixer.init()
pygame.init()
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# SETUP GAME
icon = pygame.image.load("assets/images/characters/elf/idle/0.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Hell Dungeon")
clock = pygame.time.Clock()

# define game variables
level = 1
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]

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

#load sound
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.wav")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.3)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.3)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.3)

# load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

# load potion images
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)


#load button images
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)
start_img = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)

# load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)

# Load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# Load character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

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

    #draw level
    draw_text("LEVEL: " + str(level), font,constants.WHITE, constants.SCREEN_WIDTH/2, 15)
    # show score
    draw_text(f" x{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 200, 15)

#function to reset level
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    #create empty tile list
    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)

    return data

# Create map
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

#load map files
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)





world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)


def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))




# DAMAGE TEXT CLASS
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
       pygame.sprite.Sprite.__init__(self)
       self.image = font.render(damage, True, color)
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.counter = 0
    def update(self):
        #Repos
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up
        self.rect.y -= 1
        # delete text
        self.counter += 1
        if self.counter > 30:
            self.kill()
        
# Class for screen fade
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
        elif self.direction == 2:
            pygame.draw.rect(screen, self.color, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
        return fade_complete


# CREATE PLAYER
player = world.player

# CREATE ENEMY
enemy_list = world.character_list

# CREATE PLAYER'S WEAPON
bow = Weapon(bow_image, arrow_image)


# CREATE SPRITE GROUP
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()


#add items from the level date
for item in world.item_list:
    item_group.add(item)

score_coin = Item(constants.SCREEN_WIDTH - 200, 20, 0, coin_images, True)
item_group.add(score_coin)


# Create screen fade
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

# Create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

# GAME LOOP
run = True
while run:
    # Control frame rate
    clock.tick(constants.FPS)

    if start_game == False:
        screen.fill(constants.MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game == True:
            screen.fill(constants.MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            screen.fill(constants.BG)

            if player.alive:
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
                screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tile, world.nextLv_tile)
                #print(screen_scroll)
            # UPDATE
                world.update(screen_scroll)
                for enemy in enemy_list:        
                    fireball = enemy.ai(player, world.obstacle_tile, screen_scroll, fireball_image)
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        enemy.update()        
                player.update()
                fireball_group.update(screen_scroll, player)
                arrow = bow.update(player) 
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tile, enemy_list)
                    if damage:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                        damage_text_group.add(damage_text)
                        hit_fx.play()
                damage_text_group.update()
                item_group.update(screen_scroll,player, coin_fx, heal_fx)

            # DRAW
            # Draw map level
            world.draw(screen)

            # draw enemies
            for enemy in enemy_list:
                enemy.draw(screen)


            #draw player
            player.draw(screen)

            # draw fire ball
            for fireball in fireball_group:
                fireball.draw(screen)

            #draw weapon
            for arrow in arrow_group:
                arrow.draw(screen)
            bow.draw(screen)

            for fireball in fireball_group:
                fireball.draw(screen)

            # draw text
            damage_text_group.draw(screen)

            # draw items
            item_group.draw(screen)


            draw_info()
            #show coin score
            score_coin.draw(screen)

            # check level complete
            if level_complete == True:
                start_intro = True
                level += 1
                world_data = reset_level()
                #load map files
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter = ",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temp_health = player.health
                temp_score = player.score

                player = world.player
                player.health = temp_health
                player.score = temp_score

                enemy_list = world.character_list

                score_coin = Item(constants.SCREEN_WIDTH - 200, 20, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

            #show intro
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0
            # show death
            if player.alive == False:
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level()
                        #load map files
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter = ",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animations)


                        player = world.player


                        enemy_list = world.character_list

                        score_coin = Item(constants.SCREEN_WIDTH - 200, 20, 0, coin_images, True)
                        item_group.add(score_coin)
                        for item in world.item_list:
                            item_group.add(item)

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
            if event.key == pygame.K_ESCAPE:
                pause_game = True

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
