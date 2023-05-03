import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 790

# define window
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catto-run")

font = pygame.font.SysFont('arial', 24)

# adding layers

layer_list = []
for i in range(12):
    layer_list.append(pygame.image.load(f"layers/L-{i}.png").convert_alpha())

bg_width = layer_list[0].get_width()

# tiling

tiles = math.ceil(SCREEN_WIDTH/bg_width) + 1

# parallax
scroll = [0]*12
layer_scroll_velocities = [
    0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.5, 0.7, 0.7, 0.8, 1, 1
]

vel = 1
max_vel = 8
coin_vel = 0.3

# adding sprite

sprite_walk_list = []
for i in range(8):
    sprite_walk_list.append(pygame.image.load(f"sprite/walk_{i}.png").convert_alpha())

sprite_idle_list = []
for i in range(8):
    sprite_idle_list.append(pygame.image.load(f"sprite/idleUp_{i}.png").convert_alpha())

sprite_list = [sprite_walk_list, sprite_idle_list] # final list of all sprite images
sprite_index = 0
sprite_position = (80, 480)
sprite_animation_index = 0
steps = 0

# coins
coin = pygame.image.load("coins/gold_0.png").convert_alpha()
coins_list = []

def drawLayer(image, x, y):
    # x: scroll_variable
    # y: speed_modifier
    for i in range(tiles):
        WIN.blit(image, (bg_width*i + x, 0))

    x -= vel*y # decreasing x coordinate to make them appear moving
    # reset scroll
    if abs(x) >= bg_width:
        x = 0

    return x

def drawSprite(image, position):
    # position: a tuple with (x, y) coordinates
    x, y = position
    WIN.blit(image, (x, y))

def drawCoin(image):
    # spawn at random positions
    x = 80 + random.random()*500
    y = 480 - random.random()*500
    WIN.blit(image, (x, y))

class Coin():
    def __init__(self) -> None:
        self.image = pygame.image.load("coins/gold_0.png").convert_alpha()
        self.x = random.choice([300, 350, 450, 500, 700, 800, 850, 750, 900])
        self.y = random.choice([500, 550, 600, 650])

    def drawCoin(self):
        WIN.blit(self.image, (self.x, self.y))

    def moveCoin(self):
        # want the coin to move alongside layers
        self.x -= coin_vel

    @property
    def isOut(self): # property that tells us if the coin is out of the screen
        return True if self.x<0 else False

# spawn the coins
spawn_delay = 3000 # ms
last_spawn = 0

run = True

while run:

    # logic for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # layers using drawLayer
    for i in range(12):
        scroll[i] = drawLayer(layer_list[i], scroll[i], layer_scroll_velocities[i])
        print(sprite_list, sprite_index)
        sprite_animation_index = 1/vel if vel!=0 else 0
        drawSprite(sprite_list[math.floor(sprite_animation_index)][steps], sprite_position)

        curr_time = pygame.time.get_ticks()
        if curr_time - last_spawn > spawn_delay + random.randint(0, 500):
            coin = Coin()
            coins_list.append(coin)
            last_spawn = curr_time

        for coin in coins_list:
            coin.drawCoin()
            coin.moveCoin()
            if coin.isOut:
                # we do not want to draw off-screen coins
                coins_list.remove(coin)

    keys = pygame.key.get_pressed() # getting the keypresses from the window

    # stabilize the layers
    # decide right-arrow key movement
    if keys[pygame.K_RIGHT]:
        sprite_index = 1 # we want to pick the walking_list sprites
        steps += 1
        if steps>7:
            steps=0
        if vel<max_vel:
            vel = max_vel
    else:
        if vel>0:
            vel = 0

    if keys[pygame.K_UP]:
        jump = 0
        sprite_position = (90, 350)
    else:
        sprite_position = (80, 480)



    pygame.display.update()

pygame.quit()
