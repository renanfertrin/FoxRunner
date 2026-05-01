import pygame
from const import WIDTH, HEIGHT


class ParallaxBackground:
    def __init__(self, level=1):
        path = f"assets/Images/backgrounds/level{level}/"

        def load_scaled(name):
            image = pygame.image.load(path + name).convert_alpha()

            original_width, original_height = image.get_size()

            scale_width = WIDTH / original_width
            scale_height = HEIGHT / original_height

            scale = min(scale_width, scale_height)

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            return pygame.transform.scale(image, (new_width, new_height))

        self.layers = [
            {"image": load_scaled("bg6.png"), "speed": 0.5, "x": 0},
            {"image": load_scaled("bg5.png"), "speed": 1, "x": 0},
            {"image": load_scaled("bg4.png"), "speed": 2, "x": 0},
            {"image": load_scaled("bg3.png"), "speed": 3, "x": 0},
            {"image": load_scaled("bg2.png"), "speed": 4, "x": 0},
            {"image": load_scaled("bg1.png"), "speed": 5, "x": 0},
            {"image": load_scaled("bg0.png"), "speed": 6, "x": 0},
        ]

    def update(self):
        for layer in self.layers:
            layer["x"] -= layer["speed"]

            if layer["x"] <= -layer["image"].get_width():
                layer["x"] = 0

    def draw(self, screen):
        for layer in self.layers:
            image = layer["image"]
            x = layer["x"]

            y = HEIGHT - image.get_height()

            screen.blit(image, (x, y))
            screen.blit(image, (x + image.get_width(), y))