import pygame

from const import *
from player import Player
from obstacle import Obstacle
from menu import Menu
from background import ParallaxBackground
from sound_manager import SoundManager
from score_manager import ScoreManager


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fox Runner")

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.score_manager = ScoreManager()
        self.menu = Menu(self.score_manager)

        self.sound = SoundManager()
        self.apply_volume_settings()

        self.pause_options = ["RESUME", "MAIN MENU"]
        self.pause_selected = 0

        self.end_options = ["RESTART", "MAIN MENU"]
        self.end_selected = 0

        self.score_saved = False

        self.reset_game()

    def draw_text(self, screen, size, text, color, center):
        font = pygame.font.SysFont("Lucida Sans Typewriter", size, bold=True)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=center)
        screen.blit(surf, rect)

    def draw_text_left(self, screen, size, text, color, pos):
        font = pygame.font.SysFont("Lucida Sans Typewriter", size, bold=True)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(topleft=pos)
        screen.blit(surf, rect)
        return rect

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
        self.score_saved = False

        self.pause_selected = 0
        self.end_selected = 0

    def save_current_score_once(self):
        if not self.score_saved:
            self.score_manager.add_score(self.score)
            self.score_saved = True

    def next_level(self):
        self.level += 1
        self.background = ParallaxBackground(self.level)

        self.player = Player(self.get_ground_y())
        self.obstacles.clear()
        self.spawn_timer = 0

        self.sound.play_next_level()

    def run(self):
        while self.running:
            self.clock.tick(WINDOW_FPS)
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
            self.save_current_score_once()

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

            if self.player.hitbox.colliderect(obstacle.hitbox):
                self.game_over = True
                self.save_current_score_once()
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

        self.draw_text(
            self.screen,
            FONT_SCORE_SIZE,
            str(self.score),
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 60)
        )

        self.draw_text_left(
            self.screen,
            FONT_INFO_SIZE,
            f"LEVEL {self.level}",
            COLOR_LEVEL,
            (20, 20)
        )

        self.draw_text(
            self.screen,
            FONT_INFO_SIZE,
            "SPACE = PULAR | ESC = PAUSE",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )

        if self.game_over:
            self.draw_end_screen("GAME OVER", COLOR_RED)

        if self.victory:
            self.draw_end_screen("YOU WIN!", COLOR_GREEN)

    def draw_pause_menu(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        self.draw_text(
            self.screen,
            FONT_SCORE_SIZE,
            "PAUSED",
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 150)
        )

        self.pause_option_rects = []

        for index, option in enumerate(self.pause_options):
            color = COLOR_SELECTED if index == self.pause_selected else COLOR_WHITE

            rect = self.draw_text_left(
                self.screen,
                45,
                option,
                color,
                (WINDOW_WIDTH // 2 - 160, 270 + index * 70)
            )

            self.pause_option_rects.append(rect)

        self.draw_text(
            self.screen,
            FONT_INFO_SIZE,
            "ENTER / CLICK = SELECIONAR | ESC = DESPAUSAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70)
        )

    def draw_end_screen(self, message, color):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        self.draw_text(
            self.screen,
            FONT_SCORE_SIZE,
            message,
            color,
            (WINDOW_WIDTH // 2, 150)
        )

        self.end_option_rects = []

        for index, option in enumerate(self.end_options):
            option_color = COLOR_SELECTED if index == self.end_selected else COLOR_WHITE

            rect = self.draw_text_left(
                self.screen,
                45,
                option,
                option_color,
                (WINDOW_WIDTH // 2 - 160, 270 + index * 70)
            )

            self.end_option_rects.append(rect)

        self.draw_text(
            self.screen,
            FONT_INFO_SIZE,
            "ENTER / CLICK = SELECIONAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70)
        )