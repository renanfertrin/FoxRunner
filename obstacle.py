import os
import random
import pygame

from entity import Entity

from const import WINDOW_WIDTH, LEVEL_SPEED


class Obstacle(Entity):
    def __init__(self, level=1, ground_y=520):
        super().__init__()

        self.level = level
        self.ground_y = ground_y

        self.images = self.load_images(level)

        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()

        self.rect.x = WINDOW_WIDTH
        self.rect.bottom = self.ground_y

        self.speed = LEVEL_SPEED[level]

        self.hitbox = self.create_hitbox()

    def load_images(self, level):
        folder_path = f"assets/Images/obstacles/level{level}"

        images = []

        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".png"):
                path = os.path.join(folder_path, file)

                image = pygame.image.load(path).convert_alpha()

                images.append(image)

        return images

    def create_hitbox(self):
        mask = pygame.mask.from_surface(self.image)

        rects = mask.get_bounding_rects()

        if rects:
            hitbox = rects[0].copy()

            for rect in rects[1:]:
                hitbox.union_ip(rect)

            hitbox.x += self.rect.x
            hitbox.y += self.rect.y

            hitbox.inflate_ip(
                -int(hitbox.width * 0.15),
                -int(hitbox.height * 0.10)
            )

            return hitbox

        return self.rect.copy()

    def update(self):
        self.rect.x -= self.speed
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox = self.create_hitbox()

    def draw(self, screen):
        super().draw(screen)

