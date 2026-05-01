import pygame
from const import GROUND_Y, GRAVITY, JUMP_FORCE


class Player:
    def __init__(self):
        self.image = pygame.Surface((60, 50))
        self.image.fill((220, 90, 40))

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = GROUND_Y

        self.velocity_y = 0
        self.jump_count = 0
        self.max_jumps = 2

    def jump(self):
        if self.jump_count < self.max_jumps:
            self.velocity_y = JUMP_FORCE
            self.jump_count += 1
            return True

        return False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.jump_count = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)