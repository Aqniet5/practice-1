import pygame
import sys
import math
from clock import get_time_angles

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

CENTER = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()


def draw_hand(angle, length, color):
    rad = math.radians(angle)
    x = CENTER[0] + length * math.cos(rad)
    y = CENTER[1] + length * math.sin(rad)
    pygame.draw.line(screen, color, CENTER, (x, y), 4)


while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sec_angle, min_angle = get_time_angles()

    pygame.draw.circle(screen, (0, 0, 0), CENTER, 8)

    draw_hand(sec_angle, 160, (255, 0, 0))   # seconds
    draw_hand(min_angle, 120, (0, 0, 0))     # minutes

    pygame.display.update()
    clock.tick(1)