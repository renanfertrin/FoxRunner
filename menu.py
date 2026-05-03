import pygame
from const import *


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial", FONT_TITLE_SIZE, bold=True)
        self.menu_font = pygame.font.SysFont("arial", FONT_MENU_SIZE, bold=True)
        self.info_font = pygame.font.SysFont("arial", FONT_INFO_SIZE)
        self.score_font = pygame.font.SysFont("arial", 45, bold=True)

        self.options = MENU_OPTIONS
        self.selected = 0

        self.settings_options = ["MUSIC VOLUME", "SFX VOLUME"]
        self.selected_setting = 0

        self.music_volume = 0.4
        self.sfx_volume = 0.7

        self.best_score = 0
        self.score_history = []

        self.menu_bg = pygame.image.load("assets/Images/menu/menuBg.png").convert()
        self.score_bg = pygame.image.load("assets/Images/score/scoreBg.png").convert()

        self.menu_bg = pygame.transform.scale(self.menu_bg, (WIDTH, HEIGHT))
        self.score_bg = pygame.transform.scale(self.score_bg, (WIDTH, HEIGHT))

        self.option_rects = []

        self.slider_width = 420
        self.slider_height = 18
        self.slider_x = WIDTH // 2 - self.slider_width // 2
        self.music_slider_y = 275
        self.sfx_slider_y = 365

    def handle_input(self, event, state):
        if state == "menu":
            return self.handle_menu_input(event)

        if state == "score":
            return self.handle_score_input(event)

        if state == "settings":
            return self.handle_settings_input(event)

        return None

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                return self.options[self.selected].lower()

            elif event.key == pygame.K_ESCAPE:
                return "exit"

        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
                        return self.options[self.selected].lower()

        return None

    def handle_score_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return "back"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return "back"

        return None

    def handle_settings_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                return "back"

            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % len(self.settings_options)

            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % len(self.settings_options)

            elif event.key == pygame.K_LEFT:
                self.change_selected_volume(-0.05)
                return "volume_changed"

            elif event.key == pygame.K_RIGHT:
                self.change_selected_volume(0.05)
                return "volume_changed"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.music_slider_rect().collidepoint(event.pos):
                    self.selected_setting = 0
                    self.music_volume = self.volume_from_mouse(event.pos[0])
                    return "volume_changed"

                if self.sfx_slider_rect().collidepoint(event.pos):
                    self.selected_setting = 1
                    self.sfx_volume = self.volume_from_mouse(event.pos[0])
                    return "volume_changed"

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if self.selected_setting == 0:
                    self.music_volume = self.volume_from_mouse(event.pos[0])
                    return "volume_changed"

                if self.selected_setting == 1:
                    self.sfx_volume = self.volume_from_mouse(event.pos[0])
                    return "volume_changed"

        return None

    def music_slider_rect(self):
        return pygame.Rect(
            self.slider_x,
            self.music_slider_y,
            self.slider_width,
            self.slider_height
        )

    def sfx_slider_rect(self):
        return pygame.Rect(
            self.slider_x,
            self.sfx_slider_y,
            self.slider_width,
            self.slider_height
        )

    def volume_from_mouse(self, mouse_x):
        value = (mouse_x - self.slider_x) / self.slider_width
        return max(0, min(1, value))

    def change_selected_volume(self, amount):
        if self.selected_setting == 0:
            self.music_volume = max(0, min(1, self.music_volume + amount))
        else:
            self.sfx_volume = max(0, min(1, self.sfx_volume + amount))

    def update_score(self, score):
        self.score_history.append(score)

        if score > self.best_score:
            self.best_score = score

        if len(self.score_history) > 10:
            self.score_history.pop(0)

    def draw_menu(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        title = self.title_font.render("FOX RUNNER", True, COLOR_TITLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        self.option_rects.clear()

        for i, option in enumerate(self.options):
            color = COLOR_SELECTED if i == self.selected else COLOR_OPTION
            text = self.menu_font.render(option, True, color)

            x = WIDTH // 2 - text.get_width() // 2
            y = 200 + i * 70

            screen.blit(text, (x, y))
            self.option_rects.append(text.get_rect(topleft=(x, y)))

        controls = self.info_font.render(
            "SETAS/MOUSE - NAVEGAR | ENTER/CLICK - SELECIONAR",
            True,
            COLOR_WHITE
        )
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 45))

    def draw_score(self, screen):
        screen.blit(self.score_bg, (0, 0))

        title = self.title_font.render("SCORE", True, COLOR_TITLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        best = self.score_font.render(f"MELHOR: {self.best_score}", True, COLOR_OPTION)
        screen.blit(best, (WIDTH // 2 - best.get_width() // 2, 160))

        scores = list(reversed(self.score_history))

        if not scores:
            empty = self.info_font.render("NENHUMA PARTIDA AINDA", True, COLOR_WHITE)
            screen.blit(empty, (WIDTH // 2 - empty.get_width() // 2, 250))
        else:
            for i, score in enumerate(scores):
                text = self.info_font.render(f"{i + 1}. {score}", True, COLOR_WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 240 + i * 32))

        back = self.info_font.render("ESC / ENTER / CLICK PARA VOLTAR", True, COLOR_WHITE)
        screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 45))

    def draw_settings(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        title = self.title_font.render("SETTINGS", True, COLOR_TITLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 55))

        self.draw_volume_slider(
            screen,
            label="MUSIC VOLUME",
            volume=self.music_volume,
            y=220,
            slider_y=self.music_slider_y,
            selected=self.selected_setting == 0
        )

        self.draw_volume_slider(
            screen,
            label="SFX VOLUME",
            volume=self.sfx_volume,
            y=310,
            slider_y=self.sfx_slider_y,
            selected=self.selected_setting == 1
        )

        help_text = self.info_font.render(
            "← → AJUSTAR | MOUSE - ARRASTAR A BARRA",
            True,
            COLOR_WHITE
        )
        screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT - 90))

        back = self.info_font.render("ESC / ENTER PARA VOLTAR", True, COLOR_WHITE)
        screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 45))

    def draw_volume_slider(self, screen, label, volume, y, slider_y, selected):
        color = COLOR_SELECTED if selected else COLOR_WHITE

        label_text = self.info_font.render(
            f"{label}: {int(volume * 100)}%",
            True,
            color
        )
        screen.blit(label_text, (WIDTH // 2 - label_text.get_width() // 2, y))

        bar_rect = pygame.Rect(
            self.slider_x,
            slider_y,
            self.slider_width,
            self.slider_height
        )

        filled_width = int(self.slider_width * volume)

        filled_rect = pygame.Rect(
            self.slider_x,
            slider_y,
            filled_width,
            self.slider_height
        )

        pygame.draw.rect(screen, COLOR_BLACK, bar_rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TITLE, filled_rect, border_radius=10)
        pygame.draw.rect(screen, color, bar_rect, width=3, border_radius=10)

        knob_x = self.slider_x + filled_width
        pygame.draw.circle(
            screen,
            color,
            (knob_x, slider_y + self.slider_height // 2),
            13
        )