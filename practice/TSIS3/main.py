import pygame
import sys
import random

import persistence
import racer_logic as rl

pygame.init()

WIDTH, HEIGHT = rl.WIDTH, rl.HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")

clock = pygame.time.Clock()

FONT_S = pygame.font.SysFont("Arial", 20)
FONT_M = pygame.font.SysFont("Arial", 32, bold=True)


class Game:
    def __init__(self):
        self.settings = persistence.get_settings()

        self.state = "NAME"
        self.username = ""

        self.last_score = 0
        self.last_distance = 0
        self.last_coins = 0

    def draw_text(self, text, font, color, x, y, center=True):
        image = font.render(text, True, color)

        if center:
            rect = image.get_rect(center=(x, y))
        else:
            rect = image.get_rect(topleft=(x, y))

        screen.blit(image, rect)#put on surface

    def button(self, text, y):
        rect = pygame.Rect(100, y, 200, 50)

        mouse = pygame.mouse.get_pos()

        if rect.collidepoint(mouse):#whether mouse inside rectangle
            color = (160, 160, 160)#lighter
        else:
            color = (100, 100, 100)#darker

        pygame.draw.rect(screen, color, rect)
        self.draw_text(text, FONT_S, (255, 255, 255), rect.centerx, rect.centery)

        return rect

    def name_screen(self):
        screen.fill((240, 240, 240))

        self.draw_text("Enter Name", FONT_M, (0, 0, 0), WIDTH // 2, 180)
        self.draw_text(self.username + "|", FONT_M, (0, 100, 220), WIDTH // 2, 250)
        self.draw_text("Press ENTER", FONT_S, (80, 80, 80), WIDTH // 2, 320)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username != "":#Did the player press ENTER?AND Is the username not empty?
                    self.state = "MENU"

                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]

                else:
                    if len(self.username) < 12:
                        self.username += event.unicode#handle normal typing

        pygame.display.flip()#Updates the whole screen.

    def menu(self):
        screen.fill((255, 255, 255))

        self.draw_text("RACER GAME", FONT_M, (0, 0, 0), WIDTH // 2, 100)

        play_btn = self.button("Play", 200)#Draw a button with text "Play" at y = 200.
        leaderboard_btn = self.button("Leaderboard", 270)
        settings_btn = self.button("Settings", 340)
        quit_btn = self.button("Quit", 410)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:#This checks if the player clicked the mouse.
                if play_btn.collidepoint(event.pos):#collidepoint() checks whether a point is inside a rectangle.Event.pos is the position of the mouse
                    self.state = "PLAY"

                elif leaderboard_btn.collidepoint(event.pos):
                    self.state = "LEADERBOARD"

                elif settings_btn.collidepoint(event.pos):
                    self.state = "SETTINGS"

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

    def settings_screen(self):
        screen.fill((255, 255, 255))

        self.draw_text("Settings", FONT_M, (0, 0, 0), WIDTH // 2, 80)

        sound_btn = self.button(
            f"Sound: {'ON' if self.settings['sound'] else 'OFF'}",
            170
        )

        color_btn = self.button(
            f"Color: {self.settings['car_color']}",
            240
        )

        diff_btn = self.button(
            f"Difficulty: {self.settings['difficulty']}",
            310
        )

        back_btn = self.button("Back", 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    self.settings["sound"] = not self.settings["sound"]

                elif color_btn.collidepoint(event.pos):
                    colors = ["Red", "Green", "Blue", "Yellow"]
                    index = colors.index(self.settings["car_color"])
                    self.settings["car_color"] = colors[(index + 1) % len(colors)]

                elif diff_btn.collidepoint(event.pos):
                    diffs = ["Easy", "Medium", "Hard"]
                    index = diffs.index(self.settings["difficulty"])
                    self.settings["difficulty"] = diffs[(index + 1) % len(diffs)]

                elif back_btn.collidepoint(event.pos):
                    persistence.save_settings(self.settings)
                    self.state = "MENU"

        pygame.display.flip()

    def draw_road(self):
        screen.fill((40, 130, 40))

        pygame.draw.rect(screen, (60, 60, 60), (40, 0, 320, HEIGHT))

        for x in [110, 200, 290]:#draw white dashes
            for y in range(0, HEIGHT, 80):
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 5, 40))

    def get_safe_lane(self, player):
        player_lane = min(rl.LANES, key=lambda lane: abs(lane - player.rect.centerx))#finding current position

        lanes = rl.LANES.copy()

        if player_lane in lanes and len(lanes) > 1:
            lanes.remove(player_lane)

        return random.choice(lanes)

    def clear_one_obstacle(self, obstacles):
        for obstacle in obstacles:
            obstacle.kill()
            return True

        return False

    def play(self):
        player = rl.Player(self.settings["car_color"])

        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        events = pygame.sprite.Group()

        all_sprites.add(player)

        base_speed = {
            "Easy": 4,
            "Medium": 6,
            "Hard": 8
        }[self.settings["difficulty"]]

        finish_distance = 1500

        distance = 0
        coins_collected = 0
        coin_points = 0
        bonus = 0

        active_power = None
        power_timer = 0

        slow_timer = 0

        playing = True

        while playing:
            self.draw_road()

            level = int(distance // 300)
            speed = base_speed + level

            if active_power == "Nitro":
                speed += 4

            distance += speed * 0.08

            enemy_chance = 0.015 + level * 0.004
            obstacle_chance = 0.012 + level * 0.003

            # Traffic cars
            if random.random() < enemy_chance:#gives random number between 0 and 1
                lane = self.get_safe_lane(player)
                enemy = rl.Enemy(lane, speed)
                enemies.add(enemy)#for collision
                all_sprites.add(enemy)#for drawing/updating

            # Obstacles
            if random.random() < obstacle_chance:
                lane = self.get_safe_lane(player)
                kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])

                if random.random() < 0.2:
                    obstacle = rl.MovingBarrier(lane, speed)
                else:
                    obstacle = rl.Obstacle(lane, speed, kind)

                obstacles.add(obstacle)
                all_sprites.add(obstacle)

            # Safe path event: several lanes blocked, one lane stays open
            if random.random() < 0.004:
                safe_lane = random.choice(rl.LANES)

                for lane in rl.LANES:
                    if lane != safe_lane and random.random() < 0.5:
                        obstacle = rl.Obstacle(lane, speed, "barrier")
                        obstacles.add(obstacle)
                        all_sprites.add(obstacle)

            # Coins
            if random.random() < 0.03:
                lane = random.choice(rl.LANES)
                coin = rl.Coin(lane, speed)
                coins.add(coin)
                all_sprites.add(coin)

            # Dynamic road event: nitro strip
            if random.random() < 0.004:
                lane = random.choice(rl.LANES)
                strip = rl.NitroStrip(lane, speed)
                events.add(strip)
                all_sprites.add(strip)

            # Power-ups
            if random.random() < 0.004:
                lane = random.choice(rl.LANES)
                power_type = random.choice(["Nitro", "Shield", "Repair"])
                power = rl.PowerUp(lane, speed, power_type)
                powerups.add(power)
                all_sprites.add(power)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            player.move(slow=slow_timer > 0)

            if slow_timer > 0:
                slow_timer -= 1

            enemies.update()
            obstacles.update()
            coins.update()
            powerups.update()
            events.update()

            # Coin collision
            hit_coins = pygame.sprite.spritecollide(player, coins, True)#True=Remove the coin after collision.

            for coin in hit_coins:
                coins_collected += 1
                coin_points += coin.value

            # Nitro strip collision
            if pygame.sprite.spritecollide(player, events, True):
                if active_power is None:
                    active_power = "Nitro"
                    power_timer = 180
                    bonus += 50

            # Power-up collision
            hit_powerups = pygame.sprite.spritecollide(player, powerups, True)#returns list

            for power in hit_powerups:
                if power.power_type == "Repair":
                    if self.clear_one_obstacle(obstacles):
                        bonus += 100

                elif active_power is None:
                    active_power = power.power_type

                    if active_power == "Nitro":
                        power_timer = 300

                    elif active_power == "Shield":
                        power_timer = -1#stays active by itself

                    bonus += 100

            # Enemy collision
            hit_enemy = pygame.sprite.spritecollideany(player, enemies)#Did player collide with any sprite inside the enemies group?

            if hit_enemy:
                if active_power == "Shield":
                    hit_enemy.kill()
                    active_power = None
                    power_timer = 0
                else:
                    playing = False

            # Obstacle collision
            hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

            if hit_obstacle:
                if hit_obstacle.kind == "oil":
                    slow_timer = 120
                    hit_obstacle.kill()

                elif hit_obstacle.kind == "speed_bump":
                    slow_timer = 90
                    hit_obstacle.kill()

                else:
                    if active_power == "Shield":
                        hit_obstacle.kill()#Remove this obstacle from the game groups.
                        active_power = None
                        power_timer = 0
                    else:
                        playing = False

            # Power-up timer
            if active_power == "Nitro":
                power_timer -= 1

                if power_timer <= 0:
                    active_power = None

            # Finish line
            if distance >= finish_distance:
                playing = False

            score = int(distance) + coin_points * 10 + bonus
            remaining = max(0, finish_distance - int(distance))

            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)

            self.draw_text(f"Score: {score}", FONT_S, (255, 255, 255), 10, 10, center=False)
            self.draw_text(f"Coins: {coins_collected}", FONT_S, (255, 255, 255), 10, 35, center=False)
            self.draw_text(f"Distance: {int(distance)}m", FONT_S, (255, 255, 255), 10, 60, center=False)
            self.draw_text(f"Left: {remaining}m", FONT_S, (255, 255, 255), 10, 85, center=False)

            if active_power == "Nitro":
                self.draw_text(f"Power: Nitro {power_timer // 60}s", FONT_S, (255, 200, 0), 10, 110, center=False)

            elif active_power == "Shield":
                self.draw_text("Power: Shield", FONT_S, (0, 200, 255), 10, 110, center=False)

            else:
                self.draw_text("Power: None", FONT_S, (220, 220, 220), 10, 110, center=False)

            pygame.display.flip()
            clock.tick(150)

        self.last_score = int(distance) + coin_points * 10 + bonus
        self.last_distance = int(distance)
        self.last_coins = coins_collected

        persistence.save_score(
            self.username,
            self.last_score,
            self.last_distance,
            self.last_coins
        )

        self.state = "GAME_OVER"

    def game_over(self):
        screen.fill((80, 20, 20))

        self.draw_text("GAME OVER", FONT_M, (255, 255, 255), WIDTH // 2, 120)

        self.draw_text(f"Score: {self.last_score}", FONT_S, (255, 255, 255), WIDTH // 2, 200)
        self.draw_text(f"Distance: {self.last_distance}m", FONT_S, (255, 255, 255), WIDTH // 2, 230)
        self.draw_text(f"Coins: {self.last_coins}", FONT_S, (255, 255, 255), WIDTH // 2, 260)

        retry_btn = self.button("Retry", 340)
        menu_btn = self.button("Main Menu", 410)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    self.state = "PLAY"

                elif menu_btn.collidepoint(event.pos):
                    self.state = "MENU"

        pygame.display.flip()

    def leaderboard_screen(self):
        screen.fill((255, 255, 255))

        self.draw_text("Leaderboard", FONT_M, (0, 0, 0), WIDTH // 2, 60)

        leaderboard = persistence.get_leaderboard()

        y = 120

        for i, entry in enumerate(leaderboard):
            text = f"{i + 1}. {entry['name']} | {entry['score']} pts | {entry['distance']}m"
            self.draw_text(text, FONT_S, (0, 0, 0), 25, y, center=False)
            y += 35

        back_btn = self.button("Back", 520)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    self.state = "MENU"

        pygame.display.flip()

    def run(self):
        while True:
            if self.state == "NAME":
                self.name_screen()

            elif self.state == "MENU":
                self.menu()

            elif self.state == "PLAY":
                self.play()

            elif self.state == "SETTINGS":
                self.settings_screen()

            elif self.state == "GAME_OVER":
                self.game_over()

            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()

            clock.tick(60)


game = Game()
game.run()