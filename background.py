import pygame
from const import WINDOW_WIDTH, WINDOW_HEIGHT, LEVEL_SPEED


class ParallaxBackground:
    def __init__(self, level=1):
        path = f"assets/Images/backgrounds/level{level}/"
        ground_speed = LEVEL_SPEED[level]

        def load_image(name):
            image = pygame.image.load(path + name).convert_alpha()
            return pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.layers = [
            {"image": load_image("bg6.png"), "speed": ground_speed * 0.10, "x": 0},
            {"image": load_image("bg5.png"), "speed": ground_speed * 0.20, "x": 0},
            {"image": load_image("bg4.png"), "speed": ground_speed * 0.35, "x": 0},
            {"image": load_image("bg3.png"), "speed": ground_speed * 0.50, "x": 0},
            {"image": load_image("bg2.png"), "speed": ground_speed * 0.70, "x": 0},
            {"image": load_image("bg1.png"), "speed": ground_speed * 0.85, "x": 0},
            {"image": load_image("bg0.png"), "speed": ground_speed, "x": 0},
        ]

    def update(self):
        for layer in self.layers:
            layer["x"] -= layer["speed"]

            if layer["x"] <= -WINDOW_WIDTH:
                layer["x"] = 0

    def draw(self, screen):
        for layer in self.layers:
            image = layer["image"]
            x = layer["x"]

            screen.blit(image, (x, 0))
            screen.blit(image, (x + WINDOW_WIDTH, 0))