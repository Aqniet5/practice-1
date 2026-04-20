import pygame, sys
from pygame.locals import *
import random, time

# Initializing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Other Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0 # Counter for collected coins

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(WHITE)

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

# Task: Adding randomly appearing coins
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)
    
    # Task: Showing number of collected coins in top right
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision with Coins
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
        C1.spawn() # Respawn coin upon collection

    # Collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)