import pygame

from const import *
from player import Player
from obstacle import Obstacle
from menu import Menu
from background import ParallaxBackground
from sound_manager import SoundManager


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fox Runner")

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.menu = Menu()
        self.sound = SoundManager()
        self.apply_volume_settings()

        self.font = pygame.font.SysFont("arial", FONT_SCORE_SIZE, bold=True)
        self.info_font = pygame.font.SysFont("arial", FONT_INFO_SIZE)
        self.option_font = pygame.font.SysFont("arial", 45, bold=True)

        self.pause_options = ["RESUME", "MAIN MENU"]
        self.pause_selected = 0

        self.end_options = ["RESTART", "MAIN MENU"]
        self.end_selected = 0

        self.reset_game()

    def get_ground_y(self):
        return LEVEL_GROUND_Y.get(self.level, GROUND_Y)

    def apply_volume_settings(self):
        self.sound.set_music_volume(self.menu.music_volume)
        self.sound.set_sfx_volume(self.menu.sfx_volume)

    def reset_game(self):
        self.level = 1
        self.background = ParallaxBackground(self.level)

        self.player = Player(self.get_ground_y())
        self.obstacles = []

        self.spawn_timer = 0
        self.score = 0

        self.game_over = False
        self.victory = False

        self.pause_selected = 0
        self.end_selected = 0

    def next_level(self):
        self.level += 1
        self.background = ParallaxBackground(self.level)

        self.player = Player(self.get_ground_y())
        self.obstacles.clear()
        self.spawn_timer = 0

        self.sound.play_next_level()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state in ["menu", "score", "settings"]:
                action = self.menu.handle_input(event, self.state)

                if action == "start":
                    self.reset_game()
                    self.state = "playing"

                elif action == "score":
                    self.state = "score"

                elif action == "settings":
                    self.state = "settings"

                elif action == "exit":
                    self.running = False

                elif action == "back":
                    self.state = "menu"

                elif action == "volume_changed":
                    self.apply_volume_settings()

            elif self.state == "playing":
                self.handle_game_events(event)

            elif self.state == "paused":
                self.handle_pause_events(event)

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:

            if self.game_over or self.victory:
                if event.key == pygame.K_UP:
                    self.end_selected = (self.end_selected - 1) % len(self.end_options)

                elif event.key == pygame.K_DOWN:
                    self.end_selected = (self.end_selected + 1) % len(self.end_options)

                elif event.key == pygame.K_RETURN:
                    self.execute_end_option()

                return

            if event.key == pygame.K_ESCAPE:
                self.state = "paused"

            elif event.key == pygame.K_SPACE:
                if self.player.jump():
                    self.sound.play_jump()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (self.game_over or self.victory):
                mouse_x, mouse_y = event.pos

                for index, rect in enumerate(self.end_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.end_selected = index
                        self.execute_end_option()

        elif event.type == pygame.MOUSEMOTION:
            if self.game_over or self.victory:
                mouse_x, mouse_y = event.pos

                for index, rect in enumerate(self.end_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.end_selected = index

    def handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.state = "playing"

            elif event.key == pygame.K_UP:
                self.pause_selected = (self.pause_selected - 1) % len(self.pause_options)

            elif event.key == pygame.K_DOWN:
                self.pause_selected = (self.pause_selected + 1) % len(self.pause_options)

            elif event.key == pygame.K_RETURN:
                self.execute_pause_option()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos

                for index, rect in enumerate(self.pause_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.pause_selected = index
                        self.execute_pause_option()

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

            for index, rect in enumerate(self.pause_option_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    self.pause_selected = index

    def execute_pause_option(self):
        option = self.pause_options[self.pause_selected]

        if option == "RESUME":
            self.state = "playing"

        elif option == "MAIN MENU":
            self.state = "menu"

    def execute_end_option(self):
        option = self.end_options[self.end_selected]

        if option == "RESTART":
            self.reset_game()
            self.state = "playing"

        elif option == "MAIN MENU":
            self.state = "menu"

    def update(self):
        if self.state == "menu":
            self.sound.play_music("assets/sounds/musicBg.mp3")
            return

        if self.state == "score":
            self.sound.play_music("assets/sounds/musicScore.mp3")
            return

        if self.state == "settings":
            self.sound.play_music("assets/sounds/musicBg.mp3")
            return

        if self.state in ["playing", "paused"]:
            self.sound.play_music("assets/sounds/musicLevels.mp3")

        if self.state != "playing":
            return

        if self.game_over or self.victory:
            return

        self.background.update()
        self.player.update()

        self.score += 1

        if self.level < 4 and self.score >= LEVEL_GOALS[self.level]:
            self.next_level()

        elif self.level == 4 and self.score >= LEVEL_GOALS[4]:
            self.victory = True
            self.menu.update_score(self.score)

        self.spawn_timer += 1

        if self.spawn_timer > 80:
            self.obstacles.append(
                Obstacle(
                    level=self.level,
                    ground_y=self.get_ground_y()
                )
            )
            self.spawn_timer = 0

        for obstacle in self.obstacles:
            obstacle.update()

            if self.player.rect.colliderect(obstacle.hitbox):
                self.game_over = True
                self.menu.update_score(self.score)
                self.sound.play_hit()

        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if obstacle.rect.right > 0
        ]

    def draw(self):
        if self.state == "menu":
            self.menu.draw_menu(self.screen)

        elif self.state == "score":
            self.menu.draw_score(self.screen)

        elif self.state == "settings":
            self.menu.draw_settings(self.screen)

        elif self.state in ["playing", "paused"]:
            self.draw_game()

            if self.state == "paused":
                self.draw_pause_menu()

        pygame.display.update()

    def draw_game(self):
        self.background.draw(self.screen)

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        score_shadow = self.font.render(f"{self.score}", True, COLOR_BLACK)
        score_text = self.font.render(f"{self.score}", True, COLOR_TITLE)

        score_x = WIDTH // 2 - score_text.get_width() // 2

        self.screen.blit(score_shadow, (score_x + 3, 23))
        self.screen.blit(score_text, (score_x, 20))

        level_text = self.info_font.render(f"LEVEL {self.level}", True, COLOR_LEVEL)
        self.screen.blit(level_text, (20, 20))

        controls = self.info_font.render(
            "SPACE = PULAR | ESC = PAUSE",
            True,
            COLOR_WHITE
        )
        self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 40))

        if self.game_over:
            self.draw_end_screen("GAME OVER", COLOR_RED)

        if self.victory:
            self.draw_end_screen("YOU WIN!", COLOR_GREEN)

    def draw_pause_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSED", True, COLOR_TITLE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        self.pause_option_rects = []

        for index, option in enumerate(self.pause_options):
            color = COLOR_SELECTED if index == self.pause_selected else COLOR_WHITE
            text = self.option_font.render(option, True, color)

            x = WIDTH // 2 - text.get_width() // 2
            y = 270 + index * 70

            self.screen.blit(text, (x, y))
            self.pause_option_rects.append(text.get_rect(topleft=(x, y)))

        help_text = self.info_font.render(
            "ENTER / CLICK = SELECIONAR | ESC = DESPAUSAR",
            True,
            COLOR_WHITE
        )
        self.screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT - 70))

    def draw_end_screen(self, message, color):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render(message, True, color)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        self.end_option_rects = []

        for index, option in enumerate(self.end_options):
            option_color = COLOR_SELECTED if index == self.end_selected else COLOR_WHITE
            text = self.option_font.render(option, True, option_color)

            x = WIDTH // 2 - text.get_width() // 2
            y = 270 + index * 70

            self.screen.blit(text, (x, y))
            self.end_option_rects.append(text.get_rect(topleft=(x, y)))

        help_text = self.info_font.render(
            "ENTER / CLICK = SELECIONAR",
            True,
            COLOR_WHITE
        )
        self.screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT - 70))