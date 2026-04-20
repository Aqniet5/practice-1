import pygame
import sys
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

ball = Ball(WIDTH // 2, HEIGHT // 2, 20, 25, WIDTH, HEIGHT)

clock = pygame.time.Clock()

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                ball.move(-ball.step, 0)

            elif event.key == pygame.K_RIGHT:
                ball.move(ball.step, 0)

            elif event.key == pygame.K_UP:
                ball.move(0, -ball.step)

            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.step)

    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)

    pygame.display.update()
    clock.tick(60)