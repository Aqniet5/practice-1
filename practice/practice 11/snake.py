import pygame
import random
import time

pygame.init()

# Colors
WHITE, BLACK, RED, GOLD = (255, 255, 255), (0, 0, 0), (213, 50, 80), (255, 215, 0)
WIDTH, HEIGHT = 600, 400
dis = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake_block = 10
font_style = pygame.font.SysFont("bahnschrift", 25)

def gameLoop():
    game_over = False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1
    score = 0
    
    # Timer/Weight Logic for Food
    def generate_food():
        fx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        fy = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
        weight = random.choice([1, 3]) # 1 = Red, 3 = Gold
        timer = pygame.time.get_ticks() # Timestamp of creation
        return fx, fy, weight, timer

    foodx, foody, food_w, food_timer = generate_food()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: x1_change, y1_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT: x1_change, y1_change = snake_block, 0
                elif event.key == pygame.K_UP: y1_change, x1_change = -snake_block, 0
                elif event.key == pygame.K_DOWN: y1_change, x1_change = snake_block, 0

        # Boundary Check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        # Task: Disappearing food after 5 seconds
        if pygame.time.get_ticks() - food_timer > 5000:
            foodx, foody, food_w, food_timer = generate_food()

        x1 += x1_change
        y1 += y1_change
        dis.fill(WHITE)

        # Draw food
        pygame.draw.rect(dis, GOLD if food_w == 3 else RED, [foodx, foody, snake_block, snake_block])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self-collision check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        for x in snake_List:
            pygame.draw.rect(dis, BLACK, [x[0], x[1], snake_block, snake_block])

        # Draw Score
        score_val = font_style.render(f"Score: {score}", True, BLACK)
        dis.blit(score_val, [0, 0])

        pygame.display.update()

        # Collision with food
        if x1 == foodx and y1 == foody:
            score += food_w
            Length_of_snake += food_w
            foodx, foody, food_w, food_timer = generate_food()

        clock.tick(15)

    pygame.quit()
    quit()

gameLoop()