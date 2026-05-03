import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.music_volume = 0.4
        self.sfx_volume = 0.7

        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.next_level_sound = pygame.mixer.Sound("assets/sounds/nextLevel.wav")

        self.current_music = None
        self.update_sfx_volume()

    def update_sfx_volume(self):
        self.jump_sound.set_volume(self.sfx_volume)
        self.hit_sound.set_volume(self.sfx_volume)
        self.next_level_sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))
        self.update_sfx_volume()

    def play_jump(self):
        self.jump_sound.play()

    def play_hit(self):
        self.hit_sound.play()

    def play_next_level(self):
        self.next_level_sound.play()

    def play_music(self, music_path):
        if self.current_music == music_path:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

        self.current_music = music_path