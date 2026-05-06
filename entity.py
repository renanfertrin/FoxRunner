import pygame


class Entity:
    def __init__(self):
        self.image = None
        self.rect = None
        self.hitbox = None

    def update(self):
        pass

    def draw(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen, color=(255, 0, 0)):
        if self.hitbox:
            pygame.draw.rect(screen, color, self.hitbox, 2)

    def is_out_of_screen(self):
        if self.rect:
            return self.rect.right < 0

        return False