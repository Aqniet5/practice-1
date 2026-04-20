import pygame
import time
import random

pygame.init()

# Setup
white, yellow, black, red, green = (255, 255, 255), (255, 255, 0), (0, 0, 0), (213, 50, 80), (0, 255, 0)
width, height = 600, 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
initial_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_info(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1
    score = 0
    level = 1
    speed = initial_speed

    # Task: Random position for food
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            dis.fill(white)
            msg = font_style.render("Lost! Press C-Play Again or Q-Quit", True, red)
            dis.blit(msg, [width / 6, height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change, y1_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT:
                    x1_change, y1_change = snake_block, 0
                elif event.key == pygame.K_UP:
                    y1_change, x1_change = -snake_block, 0
                elif event.key == pygame.K_DOWN:
                    y1_change, x1_change = snake_block, 0

        # Task: Checking for border collision
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_info(score, level)
        pygame.display.update()

        # Task: Increase speed and level every 3 foods
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            if score % 3 == 0:
                level += 1
                speed += 2

        clock.tick(speed)

    pygame.quit()
    quit()

gameLoop()