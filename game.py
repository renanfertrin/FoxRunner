import pygame

from const import *
from menu import Menu
from sound_manager import SoundManager
from score_manager import ScoreManager
from gameplay import Gameplay
from text_helper import draw_text, draw_text_left


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fox Runner")

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU

        self.score_manager = ScoreManager()
        self.menu = Menu(self.score_manager)

        self.sound = SoundManager()
        self.apply_volume_settings()

        self.player_name = DEFAULT_PLAYER_NAME
        self.name_input = ""

        self.gameplay = Gameplay(
            self.score_manager,
            self.sound,
            self.player_name
        )

        self.pause_options = PAUSE_OPTIONS
        self.pause_selected = 0

        self.end_options = END_OPTIONS
        self.end_selected = 0

    def apply_volume_settings(self):
        self.sound.set_music_volume(self.menu.music_volume)
        self.sound.set_sfx_volume(self.menu.sfx_volume)

    def reset_game(self):
        final_name = self.name_input.strip().upper()

        if final_name == "":
            final_name = DEFAULT_PLAYER_NAME

        self.player_name = final_name
        self.gameplay.set_player_name(self.player_name)
        self.gameplay.reset()

        self.pause_selected = 0
        self.end_selected = 0

    def start_name_input(self):
        self.name_input = ""
        self.state = STATE_NAME_INPUT

    def handle_name_input_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = STATE_MENU

            elif event.key == pygame.K_RETURN:
                self.reset_game()
                self.state = STATE_PLAYING

            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]

            elif len(self.name_input) < MAX_PLAYER_NAME_LENGTH:
                char = event.unicode.upper()

                if char.isalnum():
                    self.name_input += char

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

            if self.state in [STATE_MENU, STATE_SCORE, STATE_SETTINGS]:
                action = self.menu.handle_input(event, self.state)

                if action == "start":
                    self.start_name_input()

                elif action == "score":
                    self.state = STATE_SCORE

                elif action == "settings":
                    self.state = STATE_SETTINGS

                elif action == "exit":
                    self.running = False

                elif action == "back":
                    self.state = STATE_MENU

                elif action == "volume_changed":
                    self.apply_volume_settings()

            elif self.state == STATE_NAME_INPUT:
                self.handle_name_input_events(event)

            elif self.state == STATE_PLAYING:
                self.handle_game_events(event)

            elif self.state == STATE_PAUSED:
                self.handle_pause_events(event)

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:

            if self.gameplay.game_over or self.gameplay.victory:
                if event.key == pygame.K_UP:
                    self.end_selected = (self.end_selected - 1) % len(self.end_options)

                elif event.key == pygame.K_DOWN:
                    self.end_selected = (self.end_selected + 1) % len(self.end_options)

                elif event.key == pygame.K_RETURN:
                    self.execute_end_option()

                return

            if event.key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED

            elif event.key == pygame.K_SPACE:
                self.gameplay.jump()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (self.gameplay.game_over or self.gameplay.victory):
                mouse_x, mouse_y = event.pos

                for index, rect in enumerate(self.end_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.end_selected = index
                        self.execute_end_option()

        elif event.type == pygame.MOUSEMOTION:
            if self.gameplay.game_over or self.gameplay.victory:
                mouse_x, mouse_y = event.pos

                for index, rect in enumerate(self.end_option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.end_selected = index

    def handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.state = STATE_PLAYING

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
            self.state = STATE_PLAYING

        elif option == "MAIN MENU":
            self.state = STATE_MENU

    def execute_end_option(self):
        option = self.end_options[self.end_selected]

        if option == "RESTART":
            self.start_name_input()

        elif option == "MAIN MENU":
            self.state = STATE_MENU

    def update(self):
        if self.state == STATE_MENU:
            self.sound.play_music(PATH_MUSIC_BG)
            return

        if self.state == STATE_SCORE:
            self.sound.play_music(PATH_MUSIC_SCORE)
            return

        if self.state == STATE_SETTINGS:
            self.sound.play_music(PATH_MUSIC_BG)
            return

        if self.state == STATE_NAME_INPUT:
            self.sound.play_music(PATH_MUSIC_BG)
            return

        if self.state in [STATE_PLAYING, STATE_PAUSED]:
            self.sound.play_music(PATH_MUSIC_LEVELS)

        if self.state == STATE_PLAYING:
            self.gameplay.update()

    def draw(self):
        if self.state == STATE_MENU:
            self.menu.draw_menu(self.screen)

        elif self.state == STATE_SCORE:
            self.menu.draw_score(self.screen)

        elif self.state == STATE_SETTINGS:
            self.menu.draw_settings(self.screen)

        elif self.state == STATE_NAME_INPUT:
            self.draw_name_input()

        elif self.state in [STATE_PLAYING, STATE_PAUSED]:
            self.gameplay.draw(self.screen)

            if self.gameplay.game_over:
                self.draw_end_screen("GAME OVER", COLOR_RED)

            if self.gameplay.victory:
                self.draw_end_screen("YOU WIN!", COLOR_GREEN)

            if self.state == STATE_PAUSED:
                self.draw_pause_menu()

        pygame.display.update()

    def draw_name_input(self):
        self.screen.blit(self.menu.menu_bg, (0, 0))

        draw_text(
            self.screen,
            FONT_TITLE_SIZE,
            TEXT_NAME_INPUT_TITLE,
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 90)
        )

        name_to_show = self.name_input

        if name_to_show == "":
            name_to_show = DEFAULT_PLAYER_NAME

        draw_text(
            self.screen,
            FONT_MENU_SIZE,
            name_to_show,
            COLOR_SELECTED,
            (WINDOW_WIDTH // 2, 260)
        )

        draw_text(
            self.screen,
            FONT_INFO_SIZE,
            TEXT_NAME_INPUT_HELP,
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )

    def draw_pause_menu(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        draw_text(
            self.screen,
            FONT_SCORE_SIZE,
            "PAUSED",
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 150)
        )

        self.pause_option_rects = []

        for index, option in enumerate(self.pause_options):
            color = COLOR_SELECTED if index == self.pause_selected else COLOR_WHITE

            rect = draw_text_left(
                self.screen,
                45,
                option,
                color,
                (WINDOW_WIDTH // 2 - 160, 270 + index * 70)
            )

            self.pause_option_rects.append(rect)

        draw_text(
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

        draw_text(
            self.screen,
            FONT_SCORE_SIZE,
            message,
            color,
            (WINDOW_WIDTH // 2, 150)
        )

        self.end_option_rects = []

        for index, option in enumerate(self.end_options):
            option_color = COLOR_SELECTED if index == self.end_selected else COLOR_WHITE

            rect = draw_text_left(
                self.screen,
                45,
                option,
                option_color,
                (WINDOW_WIDTH // 2 - 160, 270 + index * 70)
            )

            self.end_option_rects.append(rect)

        draw_text(
            self.screen,
            FONT_INFO_SIZE,
            "ENTER / CLICK = SELECIONAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 70)
        )