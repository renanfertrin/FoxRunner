import pygame
from const import *


class Menu:
    def __init__(self, score_manager):
        self.score_manager = score_manager

        self.options = MENU_OPTIONS
        self.selected = 0

        self.settings_options = ["MUSIC VOLUME", "SFX VOLUME"]
        self.selected_setting = 0

        self.music_volume = 0.4
        self.sfx_volume = 0.7

        self.menu_bg = pygame.image.load("assets/Images/menu/menuBg.png").convert()
        self.score_bg = pygame.image.load("assets/Images/score/scoreBg.png").convert()

        self.menu_bg = pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.score_bg = pygame.transform.scale(self.score_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.option_rects = []

        self.slider_width = 420
        self.slider_height = 18
        self.slider_x = WINDOW_WIDTH // 2 - self.slider_width // 2

        self.music_slider_y = 265
        self.sfx_slider_y = 355

    def draw_text(self, screen, text_size, text, color, center_pos):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size, bold=True)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=center_pos)
        screen.blit(surf, rect)

    def draw_text_left(self, screen, text_size, text, color, pos):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size, bold=True)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(topleft=pos)
        screen.blit(surf, rect)
        return rect

    def handle_input(self, event, state):
        if state == "menu":
            return self.handle_menu_input(event)

        if state == "score":
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    return "back"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return "back"

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
        return pygame.Rect(self.slider_x, self.music_slider_y, self.slider_width, self.slider_height)

    def sfx_slider_rect(self):
        return pygame.Rect(self.slider_x, self.sfx_slider_y, self.slider_width, self.slider_height)

    def volume_from_mouse(self, mouse_x):
        value = (mouse_x - self.slider_x) / self.slider_width
        return max(0, min(1, value))

    def change_selected_volume(self, amount):
        if self.selected_setting == 0:
            self.music_volume = max(0, min(1, self.music_volume + amount))
        else:
            self.sfx_volume = max(0, min(1, self.sfx_volume + amount))

    def draw_menu(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        self.draw_text(
            screen,
            FONT_TITLE_SIZE,
            "FOX RUNNER",
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 90)
        )

        self.option_rects.clear()

        for i, option in enumerate(self.options):
            color = COLOR_SELECTED if i == self.selected else COLOR_OPTION

            rect = self.draw_text_left(
                screen,
                FONT_MENU_SIZE,
                option,
                color,
                (80, 170 + i * 80)
            )

            self.option_rects.append(rect)

        self.draw_text(
            screen,
            FONT_INFO_SIZE,
            "SETAS/MOUSE - NAVEGAR | ENTER/CLICK - SELECIONAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )

    def draw_score(self, screen):
        screen.blit(self.score_bg, (0, 0))

        left_x = 80

        self.draw_text_left(
            screen,
            FONT_TITLE_SIZE,
            "SCORE",
            COLOR_TITLE,
            (left_x, 60)
        )

        best = self.score_manager.get_best_score()

        self.draw_text_left(
            screen,
            42,
            f"MELHOR: {best}",
            COLOR_OPTION,
            (left_x, 160)
        )

        scores = self.score_manager.get_scores()

        if not scores:
            self.draw_text_left(
                screen,
                30,
                "SEM SCORES AINDA",
                COLOR_WHITE,
                (left_x, 240)
            )
        else:
            for i, score in enumerate(scores[:8]):
                self.draw_text_left(
                    screen,
                    30,
                    f"{i + 1:02d} - {score}",
                    COLOR_WHITE,
                    (left_x, 230 + i * 34)
                )

        self.draw_text(
            screen,
            FONT_INFO_SIZE,
            "ESC OU CLICK PARA VOLTAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )

    def draw_settings(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        self.draw_text(
            screen,
            FONT_TITLE_SIZE,
            "SETTINGS",
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 90)
        )

        self.draw_volume_slider(
            screen,
            label="MUSIC",
            volume=self.music_volume,
            y=215,
            slider_y=self.music_slider_y,
            selected=self.selected_setting == 0
        )

        self.draw_volume_slider(
            screen,
            label="SFX",
            volume=self.sfx_volume,
            y=305,
            slider_y=self.sfx_slider_y,
            selected=self.selected_setting == 1
        )

        self.draw_text(
            screen,
            FONT_INFO_SIZE,
            "UP/DOWN-SELECIONAR | LEFT/RIGHT-AJUSTAR | MOUSE-ARRASTAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 75)
        )

        self.draw_text(
            screen,
            FONT_INFO_SIZE,
            "ESC / ENTER PARA VOLTAR",
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )

    def draw_volume_slider(self, screen, label, volume, y, slider_y, selected):
        color = COLOR_SELECTED if selected else COLOR_WHITE

        self.draw_text(
            screen,
            35,
            f"{label}: {int(volume * 100)}%",
            color,
            (WINDOW_WIDTH // 2, y)
        )

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