import pygame
import os


class MusicPlayer:
    def __init__(self, folder):
        pygame.mixer.init()
        self.folder = folder
        self.playlist = [f for f in os.listdir(folder) if f.endswith(".wav")]
        self.index = 0

    def load(self):
        path = os.path.join(self.folder, self.playlist[self.index])
        pygame.mixer.music.load(path)

    def play(self):
        self.load()
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def current(self):
        return self.playlist[self.index]