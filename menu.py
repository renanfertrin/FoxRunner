import pygame
from const import WIDTH, HEIGHT


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial", 90, bold=True)
        self.menu_font = pygame.font.SysFont("arial", 60, bold=True)
        self.info_font = pygame.font.SysFont("arial", 35)
        self.score_font = pygame.font.SysFont("arial", 45, bold=True)

        self.options = ["START", "SCORE", "EXIT"]
        self.selected = 0

        self.best_score = 0
        self.score_history = []

        self.menu_bg = pygame.image.load("assets/Images/menu/menuBg.png").convert()
        self.score_bg = pygame.image.load("assets/Images/score/scoreBg.png").convert()

        self.menu_bg = pygame.transform.scale(self.menu_bg, (WIDTH, HEIGHT))
        self.score_bg = pygame.transform.scale(self.score_bg, (WIDTH, HEIGHT))

    def handle_input(self, event, state):
        if event.type == pygame.KEYDOWN:

            if state == "menu":
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected].lower()

            elif state == "score":
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    return "back"

        return None

    def update_score(self, score):
        self.score_history.append(score)

        if score > self.best_score:
            self.best_score = score

        if len(self.score_history) > 10:
            self.score_history.pop(0)

    def draw_menu(self, screen):
        screen.blit(self.menu_bg, (0, 0))

        # 🔥 COR ALTERADA AQUI
        title = self.title_font.render("FOX RUNNER", True, (242, 155, 53))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (0, 255, 255)
            text = self.menu_font.render(option, True, color)

            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 90))

        controls = self.info_font.render(
            "ENTER - SELECIONAR",
            True,
            (255, 255, 255)
        )
        screen.blit(
            controls,
            (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 60)
        )

    def draw_score(self, screen):
        screen.blit(self.score_bg, (0, 0))

        title = self.title_font.render("SCORE", True, (242, 155, 53))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        best = self.score_font.render(
            f"MELHOR: {self.best_score}",
            True,
            (0, 255, 200)
        )
        screen.blit(best, (WIDTH // 2 - best.get_width() // 2, 180))

        scores = list(reversed(self.score_history))

        for i, score in enumerate(scores):
            text = self.score_font.render(
                f"{i+1}. {score}",
                True,
                (255, 255, 255)
            )
            screen.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, 260 + i * 45)
            )

        back = self.info_font.render(
            "ESC / ENTER PARA VOLTAR",
            True,
            (255, 255, 255)
        )
        screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 60))