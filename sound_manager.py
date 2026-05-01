import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.next_level_sound = pygame.mixer.Sound("assets/sounds/nextLevel.wav")

        self.current_music = None

    def play_jump(self):
        self.jump_sound.play()

    def play_hit(self):
        self.hit_sound.play()

    def play_next_level(self):
        self.next_level_sound.play()

    def play_music(self, music_path):
        # se já estiver tocando essa música, não reinicia
        if self.current_music == music_path:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.4)

        # 🔥 LOOP INFINITO AQUI
        pygame.mixer.music.play(-1)

        self.current_music = music_path

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None