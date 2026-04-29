import pygame
import random
import sys
import json
import os

from config import *
from db import DBHandler


SETTINGS_FILE = "settings.json"


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake")
        self.clock = pygame.time.Clock()

        self.db = DBHandler()
        self.settings = self.load_settings()

        self.state = "MENU"
        self.username = ""
        self.message = ""
        self.best = 0
        self.leaderboard = []

        self.reset_game()

    def load_settings(self):
        settings = {
            "snake_color": [0, 200, 0],
            "grid_overlay": True,
            "sound": False
        }

        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings.update(json.load(f))

        return settings

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=4)

    def reset_game(self):
        self.snake = [(100, TOP + 40), (80, TOP + 40), (60, TOP + 40)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.food_count = 0

        self.obstacles = []
        self.food = None
        self.poison = None
        self.power = None

        self.shield = False
        self.speed_effect = 0
        self.effect_end = 0

        self.saved = False#prevents game result many times
        self.last_move = pygame.time.get_ticks()#returns miliseconds since Pygame started
        self.next_power_time = pygame.time.get_ticks() + 5000

        self.food = self.spawn_food()
        self.poison = self.random_empty_cell()

    def text(self, msg, size, color, x, y, center=True):
        font = pygame.font.SysFont("Arial", size)
        img = font.render(str(msg), True, color)#smoothly not pixelated,turn text into img

        if center:
            rect = img.get_rect(center=(x, y))#rectangle object
        else:
            rect = img.get_rect(topleft=(x, y))

        self.screen.blit(img, rect)#draw the image onto the screen

    def button(self, msg, y, w=240):
        rect = pygame.Rect(WIDTH // 2 - w // 2, y, w, 45)
        pygame.draw.rect(self.screen, DARK, rect, border_radius=8)
        self.text(msg, 23, WHITE, rect.centerx, rect.centery)
        return rect

    def all_cells(self):
        cells = []

        for x in range(0, WIDTH, CELL):
            for y in range(TOP, HEIGHT, CELL):
                cells.append((x, y))

        return cells

    def random_empty_cell(self, extra_blocked=None):
        blocked = set(self.snake)#set of snake's body
        blocked.update(self.obstacles)#adds obstacle positions

        if self.food:
            blocked.add(self.food["pos"])#food is dict and has pos,weight,born

        if self.poison:
            blocked.add(self.poison)

        if self.power:
            blocked.add(self.power["pos"])#power is dict and has pos,type,time

        if extra_blocked:
            blocked.update(extra_blocked)

        free = [cell for cell in self.all_cells() if cell not in blocked]

        return random.choice(free)

    def spawn_food(self):
        return {
            "pos": self.random_empty_cell(),
            "weight": random.choice([1, 1, 2, 3]),
            "born": pygame.time.get_ticks()#to check later for timer of food
        }

    def spawn_power(self):
        self.power = {
            "pos": self.random_empty_cell(),
            "type": random.choice(["BOOST", "SLOW", "SHIELD"]),
            "born": pygame.time.get_ticks()
        }

    def make_obstacles(self):
        if self.level < 3:
            return

        self.obstacles = []#removes old obstacles before creating new

        head = self.snake[0]
        safe = {head}

        for dx, dy in [(CELL, 0), (-CELL, 0), (0, CELL), (0, -CELL)]:
            safe.add((head[0] + dx, head[1] + dy))#shouldnt be obstacles around snake because it will get trapped

        amount = min(5 + self.level * 2, 35)#amount of obstacles

        while len(self.obstacles) < amount:
            block = self.random_empty_cell(extra_blocked=safe)

            if block not in safe and block not in self.obstacles:
                self.obstacles.append(block)#adding new position to obstacle's list

    def inside_field(self, pos):
        x, y = pos
        return 0 <= x < WIDTH and TOP <= y < HEIGHT

    def wrap(self, pos):#moves the snake to the opposite side if shield is active and it hits a wall.
        x, y = pos

        if x < 0:
            x = WIDTH - CELL
        elif x >= WIDTH:
            x = 0

        if y < TOP:
            y = HEIGHT - CELL
        elif y >= HEIGHT:
            y = TOP

        return (x, y)

    def current_speed(self):
        return max(4, 8 + self.level + self.speed_effect)

    def activate_power(self, power_type):
        now = pygame.time.get_ticks()

        if power_type == "BOOST":
            self.speed_effect = 5
            self.effect_end = now + 5000

        elif power_type == "SLOW":
            self.speed_effect = -4
            self.effect_end = now + 5000

        elif power_type == "SHIELD":
            self.shield = True

    def finish_game(self):#save result and go to Game Over screen
        if not self.saved:#Without this check, the same score could be inserted into the database multiple times.
            name = self.username.strip()
            self.db.save_session(name, self.score, self.level)
            self.best = self.db.get_best_score(name)
            self.saved = True

        self.state = "GAME_OVER"

    def move(self):#start of snake movement logic
        if self.next_direction != (-self.direction[0], -self.direction[1]):#This prevents the snake from instantly reversing into itself.
            self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if not self.inside_field(new_head):
            if self.shield:
                self.shield = False
                new_head = self.wrap(new_head)
            else:
                self.finish_game()
                return

        # Obstacle collision
        if new_head in self.obstacles:
            if self.shield:
                self.shield = False
                self.obstacles.remove(new_head)
            else:
                self.finish_game()
                return

        ate_food = self.food and new_head == self.food["pos"]

        if ate_food:
            body = self.snake
        else:
            body = self.snake[:-1]#When snake moves normally, the tail disappears.

        # Self collision
        if new_head in body:
            if self.shield:
                self.shield = False
            else:
                self.finish_game()
                return

        self.snake.insert(0, new_head)

        # Normal food
        if ate_food:
            self.score += self.food["weight"] * 10
            self.food_count += 1
            self.food = self.spawn_food()

            if self.food_count % 5 == 0:
                self.level += 1
                self.make_obstacles()
        else:
            self.snake.pop()#If the snake did not eat food, we remove the last part to keep the same length.

        # Poison food
        if self.poison and new_head == self.poison:
            for _ in range(2):
                if self.snake:
                    self.snake.pop()

            self.poison = self.random_empty_cell()

            if len(self.snake) <= 1:
                self.finish_game()
                return

        # Power-up
        if self.power and new_head == self.power["pos"]:
            self.activate_power(self.power["type"])
            self.power = None#After the snake collects the power-up, it should disappear from the map.
            self.next_power_time = pygame.time.get_ticks() + 6000#Spawn the next power-up after 6 seconds.

    def update_game(self):
        now = pygame.time.get_ticks()

        if now - self.food["born"] > 7000:
            self.food = self.spawn_food()

        if self.power:
            if now - self.power["born"] > 8000:
                self.power = None
                self.next_power_time = now + 5000#Wait 5 seconds before spawning the next power-up.
        else:
            if now >= self.next_power_time:
                self.spawn_power()

        if self.speed_effect != 0 and now >= self.effect_end:
            self.speed_effect = 0

        delay = 1000 // self.current_speed()#This calculates how many milliseconds should pass before snake moves again.

        if now - self.last_move >= delay:
            self.move()
            self.last_move = now

    def draw_grid(self):#A grid means the game field is divided into equal squares.
        if not self.settings["grid_overlay"]:
            return

        for x in range(0, WIDTH, CELL):#draw vertical lines
            pygame.draw.line(self.screen, (220, 220, 220), (x, TOP), (x, HEIGHT))#starting point,ending point

        for y in range(TOP, HEIGHT, CELL):#draw horizontal lines
            pygame.draw.line(self.screen, (220, 220, 220), (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(WHITE)

        self.text(f"Score: {self.score}", 22, BLACK, 10, 15, False)
        self.text(f"Level: {self.level}", 22, BLACK, 150, 15, False)
        self.text(f"Best: {self.best}", 22, BLACK, 270, 15, False)
        self.text(f"Shield: {'ON' if self.shield else 'OFF'}", 22, BLACK, 410, 15, False)

        if self.speed_effect > 0:
            self.text("BOOST", 22, BLUE, 570, 15, False)
        elif self.speed_effect < 0:
            self.text("SLOW", 22, PURPLE, 570, 15, False)

        self.draw_grid()

        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*block, CELL, CELL))

        food_color = RED

        if self.food["weight"] == 2:
            food_color = YELLOW
        elif self.food["weight"] == 3:
            food_color = BLUE

        pygame.draw.rect(self.screen, food_color, (*self.food["pos"], CELL, CELL))
        pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL, CELL))

        if self.power:
            power_color = GREEN

            if self.power["type"] == "BOOST":
                power_color = BLUE
            elif self.power["type"] == "SLOW":
                power_color = PURPLE
            elif self.power["type"] == "SHIELD":
                power_color = YELLOW

            pygame.draw.rect(self.screen, power_color, (*self.power["pos"], CELL, CELL))

        for part in self.snake:
            pygame.draw.rect(self.screen, tuple(self.settings["snake_color"]), (*part, CELL, CELL))

    def start_game(self):
        self.best = self.db.get_best_score(self.username.strip())
        self.reset_game()
        self.state = "PLAY"

    def menu_screen(self):
        self.screen.fill(WHITE)

        self.text("Snake Game", 46, BLACK, WIDTH // 2, 70)
        self.text("Username:", 24, BLACK, WIDTH // 2, 135)

        box = pygame.Rect(WIDTH // 2 - 150, 160, 300, 45)
        pygame.draw.rect(self.screen, WHITE, box)
        pygame.draw.rect(self.screen, BLACK, box, 2)

        self.text(self.username if self.username else "_", 24, BLACK, WIDTH // 2, box.centery)

        play = self.button("Play", 240)
        board = self.button("Leaderboard", 300)
        settings = self.button("Settings", 360)
        quit_btn = self.button("Quit", 420)

        if self.message:
            self.text(self.message, 20, RED, WIDTH // 2, 500)#If there is a message, draw it on the screen.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN and self.username.strip():
                    self.start_game()
                elif len(self.username) < 12 and event.unicode.isprintable():
                    self.username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(event.pos):
                    if self.username.strip():
                        self.start_game()
                    else:
                        self.message = "Enter username first"

                elif board.collidepoint(event.pos):
                    self.leaderboard = self.db.get_top_scores()
                    self.state = "LEADERBOARD"

                elif settings.collidepoint(event.pos):
                    self.state = "SETTINGS"

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    def play_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.next_direction = (0, -CELL)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.next_direction = (0, CELL)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.next_direction = (-CELL, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.next_direction = (CELL, 0)

        self.update_game()
        self.draw_game()

    def game_over_screen(self):
        self.screen.fill(WHITE)

        self.text("Game Over", 46, RED, WIDTH // 2, 120)
        self.text(f"Final Score: {self.score}", 28, BLACK, WIDTH // 2, 190)
        self.text(f"Level Reached: {self.level}", 28, BLACK, WIDTH // 2, 230)
        self.text(f"Personal Best: {self.best}", 28, BLACK, WIDTH // 2, 270)

        retry = self.button("Retry", 350)
        menu = self.button("Main Menu", 410)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(event.pos):
                    self.start_game()
                elif menu.collidepoint(event.pos):
                    self.state = "MENU"

    def leaderboard_screen(self):
        self.screen.fill(WHITE)

        self.text("Leaderboard", 42, BLACK, WIDTH // 2, 60)

        self.text("Rank", 20, BLACK, 50, 115, False)
        self.text("Name", 20, BLACK, 130, 115, False)
        self.text("Score", 20, BLACK, 320, 115, False)
        self.text("Level", 20, BLACK, 430, 115, False)
        self.text("Date", 20, BLACK, 540, 115, False)

        y = 155

        for i, row in enumerate(self.leaderboard):
            name, score, level, date = row

            self.text(i + 1, 20, BLACK, 60, y, False)
            self.text(name, 20, BLACK, 130, y, False)
            self.text(score, 20, BLACK, 320, y, False)
            self.text(level, 20, BLACK, 440, y, False)
            self.text(date, 20, BLACK, 540, y, False)

            y += 35

        back = self.button("Back", 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    self.state = "MENU"

    def settings_screen(self):
        self.screen.fill(WHITE)

        self.text("Settings", 42, BLACK, WIDTH // 2, 80)#title

        grid = self.button(f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}", 170)
        sound = self.button(f"Sound: {'ON' if self.settings['sound'] else 'OFF'}", 230)
        color = self.button("Change Snake Color", 290)
        save = self.button("Save & Back", 390)

        pygame.draw.rect(
            self.screen,
            tuple(self.settings["snake_color"]),
            (WIDTH // 2 - 30, 345, 60, 35)
        )

        colors = [
            [0, 200, 0],
            [0, 120, 255],
            [240, 220, 0],
            [160, 0, 200],
            [255, 120, 0]
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid.collidepoint(event.pos):
                    self.settings["grid_overlay"] = not self.settings["grid_overlay"]

                elif sound.collidepoint(event.pos):
                    self.settings["sound"] = not self.settings["sound"]

                elif color.collidepoint(event.pos):
                    current = self.settings["snake_color"]

                    if current in colors:
                        index = colors.index(current)
                    else:
                        index = 0

                    self.settings["snake_color"] = colors[(index + 1) % len(colors)]

                elif save.collidepoint(event.pos):
                    self.save_settings()
                    self.state = "MENU"

    def run(self):
        while True:
            if self.state == "MENU":
                self.menu_screen()

            elif self.state == "PLAY":
                self.play_screen()

            elif self.state == "GAME_OVER":
                self.game_over_screen()

            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()

            elif self.state == "SETTINGS":
                self.settings_screen()

            pygame.display.flip()
            self.clock.tick(FPS)