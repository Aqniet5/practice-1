import pygame
import random

WIDTH, HEIGHT = 400, 600
LANES = [65, 155, 245, 335]


def get_color(name):
    colors = {
        "Red": (220, 0, 0),
        "Green": (0, 170, 0),
        "Blue": (0, 80, 220),
        "Yellow": (230, 220, 0)
    }

    return colors.get(name, (220, 0, 0))


class Player(pygame.sprite.Sprite):#sprite is the game object
    def __init__(self, color_name):
        super().__init__()

        self.image = pygame.Surface((45, 75))
        self.image.fill(get_color(color_name))

        self.rect = self.image.get_rect(center=(200, 520))
        self.speed = 7

    def move(self, slow=False):
        keys = pygame.key.get_pressed()

        speed = self.speed
        if slow:
            speed = 4

        if keys[pygame.K_LEFT] and self.rect.left > 40:
            self.rect.x -= speed

        if keys[pygame.K_RIGHT] and self.rect.right < 360:
            self.rect.x += speed


class RoadObject(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, speed):
        super().__init__()

        self.image = pygame.Surface((w, h))
        self.image.fill(color)

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):#y increases object goes downward
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Enemy(RoadObject):
    def __init__(self, lane, speed):
        super().__init__(lane, -60, 45, 75, (40, 40, 40), speed)


class Coin(RoadObject):
    def __init__(self, lane, speed):
        super().__init__(lane, -30, 25, 25, (255, 215, 0), speed)

        self.value = random.choice([1, 1, 1, 3, 5])


class Obstacle(RoadObject):
    def __init__(self, lane, speed, kind):
        self.kind = kind#obstacle type

        colors = {
            "barrier": (160, 40, 40),
            "oil": (20, 20, 80),
            "pothole": (80, 50, 30),
            "speed_bump": (230, 160, 30)
        }

        super().__init__(lane, -40, 55, 35, colors[kind], speed)


class MovingBarrier(Obstacle):
    def __init__(self, lane, speed):
        super().__init__(lane, speed, "barrier")
        self.side_speed = random.choice([-2, 2])

    def update(self):
        super().update()

        self.rect.x += self.side_speed

        if self.rect.left < 40 or self.rect.right > 360:
            self.side_speed *= -1#changes direction


class NitroStrip(RoadObject):
    def __init__(self, lane, speed):
        super().__init__(lane, -30, 60, 25, (0, 220, 255), speed)


class PowerUp(RoadObject):
    def __init__(self, lane, speed, power_type):
        self.power_type = power_type
        self.life = 300

        colors = {
            "Nitro": (255, 130, 0),
            "Shield": (0, 100, 255),
            "Repair": (0, 220, 0)
        }

        super().__init__(lane, -30, 30, 30, colors[power_type], speed)
#To reuse parent code and add extra child behavior without copying code.
    def update(self):
        super().update()
#lifetime is a countdown timer for the power-up.
#Every frame, subtract 1 from its life.
        self.life -= 1

        if self.life <= 0:
            self.kill()