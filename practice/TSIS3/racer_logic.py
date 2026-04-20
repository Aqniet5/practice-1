import pygame
import random

class Traffic(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((200, 0, 0)) # Red Traffic
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 350), -100)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['nitro', 'shield', 'repair'])
        self.image = pygame.Surface((30, 30))
        # Gold for Nitro, Cyan for Shield, Green for Repair
        color = (255,215,0) if self.type == 'nitro' else (0,255,255) if self.type == 'shield' else (0,255,0)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 350), -50)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > 600: self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 30))
        self.image.fill((100, 100, 100)) # Grey Oil/Pothole
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 350), -50)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > 600: self.kill()