import os
import pygame

from const import (
    GRAVITY,
    JUMP_FORCE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_X,
    PLAYER_ANIMATION_SPEED
)


class Player:
    def __init__(self, ground_y):
        self.ground_y = ground_y

        self.animations = {
            "run": self.load_images("assets/Images/character/run"),
            "jump": self.load_images("assets/Images/character/jump"),
        }

        self.state = "run"
        self.frame_index = 0
        self.animation_speed = PLAYER_ANIMATION_SPEED

        self.image = self.animations["run"][0]
        self.rect = self.image.get_rect()

        self.rect.x = PLAYER_X
        self.rect.bottom = self.ground_y

        self.hitbox = self.rect.copy()

        self.velocity_y = 0
        self.jumps = 0
        self.max_jumps = 2

    def load_images(self, folder_path):
        images = []
        files = sorted(os.listdir(folder_path))

        for file in files:
            if file.endswith(".png"):
                path = os.path.join(folder_path, file)
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                images.append(image)

        return images

    def jump(self):
        if self.jumps < self.max_jumps:
            self.velocity_y = JUMP_FORCE
            self.jumps += 1
            return True
        return False

    def update(self):
        self.apply_gravity()
        self.update_state()
        self.animate()
        self.update_hitbox()

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.jumps = 0

    def update_state(self):
        if self.rect.bottom < self.ground_y:
            self.state = "jump"
        else:
            self.state = "run"

    def animate(self):
        self.frame_index += self.animation_speed

        if self.state == "run":
            if self.frame_index >= len(self.animations["run"]):
                self.frame_index = 0

            frame = self.animations["run"][int(self.frame_index)]
        else:
            total_frames = len(self.animations["jump"])

            if self.frame_index >= total_frames:
                self.frame_index = total_frames - 1

            frame = self.animations["jump"][int(self.frame_index)]

        old_bottom = self.rect.bottom
        old_x = self.rect.x

        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.bottom = old_bottom

    def update_hitbox(self):
        self.hitbox = self.rect.copy()

        self.hitbox.inflate_ip(
            -int(self.rect.width * 0.3),
            -int(self.rect.height * 0.2)
        )

        self.hitbox.y += int(self.rect.height * 0.05)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # HITBOX DO PLAYER
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)