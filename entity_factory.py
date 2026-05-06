from player import Player
from obstacle import Obstacle
from background import ParallaxBackground


class EntityFactory:
    @staticmethod
    def create_player(ground_y):
        return Player(ground_y)

    @staticmethod
    def create_obstacle(level, ground_y):
        return Obstacle(level=level, ground_y=ground_y)

    @staticmethod
    def create_background(level):
        return ParallaxBackground(level)