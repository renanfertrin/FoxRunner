class Entity:
    def __init__(self):
        self.image = None
        self.rect = None

    def update(self):
        pass

    def draw(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)