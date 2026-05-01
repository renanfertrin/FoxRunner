import pygame
from const import WIDTH, GROUND_Y


class Obstacle:
    def __init__(self, level=1):
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.bottom = GROUND_Y

        # 🔥 velocidade baseada no level
        base_speed = 6
        self.speed = base_speed + (level * 2)

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)