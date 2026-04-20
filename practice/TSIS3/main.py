import pygame, sys, random
from persistence import *
from ui import *
from racer_logic import *

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load Settings
settings = load_data('settings.json', {"sound": True, "color": "Blue", "diff": "Normal"})
username = input("Enter Username: ") # Simple console entry for requirement 3.4

def game_loop():
    running = True
    score = 0
    distance = 0
    speed = 5
    active_power = None
    power_timer = 0
    
    player_rect = pygame.Rect(180, 500, 40, 60)
    player_color = (0, 0, 255) if settings['color'] == "Blue" else (0, 255, 0)
    
    traffic = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    
    while running:
        screen.fill((200, 200, 200)) # Road color
        current_time = pygame.time.get_ticks()

        # Difficulty Scaling
        speed = 5 + (distance // 2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        move_speed = 10 if active_power == 'nitro' else 5
        if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= move_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH: player_rect.x += move_speed

        # Spawning
        if random.randint(1, 60) == 1: traffic.add(Traffic(speed + 2))
        if random.randint(1, 300) == 1: powerups.add(PowerUp())
        if random.randint(1, 150) == 1: hazards.add(Hazard())

        # Updates
        traffic.update()
        powerups.update(speed)
        hazards.update(speed)
        distance += speed // 2

        # Collision Logic
        if pygame.Rect.collidelist(player_rect, [t.rect for t in traffic]) != -1:
            if active_power == 'shield':
                active_power = None
                traffic.empty() # Clear threat
            else:
                update_leaderboard(username, score + (distance // 10))
                return "GAMEOVER"

        # Powerup collection
        for p in powerups:
            if player_rect.colliderect(p.rect):
                active_power = p.type
                power_timer = current_time
                p.kill()

        # Nitro timer
        if active_power == 'nitro' and current_time - power_timer > 5000:
            active_power = None

        # Drawing
        pygame.draw.rect(screen, player_color, player_rect)
        traffic.draw(screen)
        powerups.draw(screen)
        hazards.draw(screen)
        
        draw_text(screen, f"Score: {score}", 20, 50, 30)
        draw_text(screen, f"Dist: {distance}m", 20, 50, 60)
        if active_power: draw_text(screen, f"BUF: {active_power.upper()}", 20, 200, 30, (255,0,0))

        pygame.display.flip()
        clock.tick(60)

# Simplified Menu State
state = "MENU"
while True:
    if state == "MENU":
        screen.fill((255, 255, 255))
        draw_text(screen, "RACER ADVANCED", 40, 200, 100)
        if button(screen, "PLAY", 150, 200, 100, 50, (0,200,0), (0,255,0), lambda: "START"):
            state = game_loop()
    elif state == "GAMEOVER":
        screen.fill((0,0,0))
        draw_text(screen, "CRASHED!", 50, 200, 200, (255,0,0))
        if button(screen, "MENU", 150, 350, 100, 50, (200,0,0), (255,0,0), lambda: "MENU"):
            state = "MENU"
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
    pygame.display.flip()