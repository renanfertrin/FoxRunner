from const import *
from entity_factory import EntityFactory
from text_helper import draw_text, draw_text_left


class Gameplay:
    def __init__(self, score_manager, sound, player_name=DEFAULT_PLAYER_NAME):
        self.score_manager = score_manager
        self.sound = sound
        self.player_name = player_name
        self.reset()

    def set_player_name(self, player_name):
        name = player_name.strip().upper()

        if name == "":
            name = DEFAULT_PLAYER_NAME

        self.player_name = name

    def get_ground_y(self):
        return LEVEL_GROUND_Y.get(self.level, GROUND_Y)

    def reset(self):
        self.level = 1
        self.background = EntityFactory.create_background(self.level)

        self.player = EntityFactory.create_player(self.get_ground_y())
        self.obstacles = []

        self.spawn_timer = 0
        self.score = 0

        self.game_over = False
        self.victory = False
        self.score_saved = False

    def save_score_once(self):
        if not self.score_saved:
            self.score_manager.add_score(self.score, self.player_name)
            self.score_saved = True

    def next_level(self):
        self.level += 1
        self.background = EntityFactory.create_background(self.level)

        self.player = EntityFactory.create_player(self.get_ground_y())
        self.obstacles.clear()
        self.spawn_timer = 0

        self.sound.play_next_level()

    def jump(self):
        if not self.game_over and not self.victory:
            if self.player.jump():
                self.sound.play_jump()

    def update(self):
        if self.game_over or self.victory:
            return

        self.background.update()
        self.player.update()

        self.score += 1

        if self.level < 4 and self.score >= LEVEL_GOALS[self.level]:
            self.next_level()

        elif self.level == 4 and self.score >= LEVEL_GOALS[4]:
            self.victory = True
            self.save_score_once()

        self.spawn_timer += 1

        if self.spawn_timer > OBSTACLE_SPAWN_TIME:
            self.obstacles.append(
                EntityFactory.create_obstacle(
                    level=self.level,
                    ground_y=self.get_ground_y()
                )
            )
            self.spawn_timer = 0

        for obstacle in self.obstacles:
            obstacle.update()

            if self.player.hitbox.colliderect(obstacle.hitbox):
                self.game_over = True
                self.save_score_once()
                self.sound.play_hit()

        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if obstacle.rect.right > 0
        ]

    def draw(self, screen):
        self.background.draw(screen)
        self.player.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        draw_text(
            screen,
            FONT_SCORE_SIZE,
            str(self.score),
            COLOR_TITLE,
            (WINDOW_WIDTH // 2, 60)
        )

        draw_text_left(
            screen,
            FONT_INFO_SIZE,
            f"LEVEL {self.level}",
            COLOR_LEVEL,
            (20, 20)
        )

        draw_text(
            screen,
            FONT_INFO_SIZE,
            TEXT_GAME_HELP,
            COLOR_WHITE,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )