import pygame

from const import WIDTH, HEIGHT, FPS
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

        self.font = pygame.font.SysFont("arial", 70, bold=True)
        self.info_font = pygame.font.SysFont("arial", 30)

        self.level_goals = {
            1: 1000,
            2: 2000,
            3: 3500,
            4: 5000
        }

        self.reset_game()

    def reset_game(self):
        self.level = 1
        self.background = ParallaxBackground(self.level)

        self.player = Player()
        self.obstacles = []

        self.spawn_timer = 0
        self.score = 0

        self.game_over = False
        self.victory = False

    def next_level(self):
        self.level += 1
        self.background = ParallaxBackground(self.level)

        self.player = Player()
        self.obstacles.clear()
        self.spawn_timer = 0

        # 🔥 SOM AO TROCAR DE FASE
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

            if self.state in ["menu", "score"]:
                action = self.menu.handle_input(event, self.state)

                if action == "start":
                    self.reset_game()
                    self.state = "playing"

                elif action == "score":
                    self.state = "score"

                elif action == "exit":
                    self.running = False

                elif action == "back":
                    self.state = "menu"

            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"

                    if not self.game_over and not self.victory:
                        if event.key == pygame.K_SPACE:
                            if self.player.jump():
                                self.sound.play_jump()

                    if self.game_over or self.victory:
                        if event.key == pygame.K_r:
                            self.state = "menu"

    def update(self):
        if self.state == "menu":
            self.sound.play_music("assets/sounds/musicBg.mp3")
            return

        if self.state == "score":
            self.sound.play_music("assets/sounds/musicScore.mp3")
            return

        if self.state != "playing":
            return

        self.sound.play_music("assets/sounds/musicLevels.mp3")

        if self.game_over or self.victory:
            return

        self.background.update()
        self.player.update()

        self.score += 1

        if self.level < 4 and self.score >= self.level_goals[self.level]:
            self.next_level()

        elif self.level == 4 and self.score >= self.level_goals[4]:
            self.victory = True
            self.menu.update_score(self.score)

        self.spawn_timer += 1

        if self.spawn_timer > 80:
            self.obstacles.append(Obstacle(self.level))
            self.spawn_timer = 0

        for obstacle in self.obstacles:
            obstacle.update()

            if self.player.rect.colliderect(obstacle.rect):
                self.game_over = True
                self.menu.update_score(self.score)
                self.sound.play_hit()

    def draw(self):
        if self.state == "menu":
            self.menu.draw_menu(self.screen)

        elif self.state == "score":
            self.menu.draw_score(self.screen)

        elif self.state == "playing":
            self.draw_game()

        pygame.display.update()

    def draw_game(self):
        self.background.draw(self.screen)

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        score_shadow = self.font.render(f"{self.score}", True, (0, 0, 0))
        score_text = self.font.render(f"{self.score}", True, (242, 155, 53))

        x = WIDTH // 2 - score_text.get_width() // 2

        self.screen.blit(score_shadow, (x + 3, 23))
        self.screen.blit(score_text, (x, 20))

        level_text = self.info_font.render(f"LEVEL {self.level}", True, (242, 155, 53))
        self.screen.blit(level_text, (20, 20))

        controls = self.info_font.render(
            "SPACE = PULAR | ESC = MENU",
            True,
            (255, 255, 255)
        )
        self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 40))

        if self.game_over:
            text = self.font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

        if self.victory:
            text = self.font.render("YOU WIN!", True, (0, 255, 0))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))