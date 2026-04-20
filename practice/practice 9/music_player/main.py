import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

player = MusicPlayer("music")

running = True

while running:
    screen.fill((30, 30, 30))

    text = font.render(f"Track: {player.current()}", True, (255, 255, 255))
    screen.blit(text, (20, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next()

            elif event.key == pygame.K_b:
                player.prev()

            elif event.key == pygame.K_q:
                running = False

    pygame.display.update()

pygame.quit()