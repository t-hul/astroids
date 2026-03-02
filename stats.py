import pygame
from constants import SCORE_MAX_PER_SECOND, SCORE_PER_SPLIT, ASTERIOD_MAX_DENSITY


class Stats(pygame.sprite.Sprite):
    def __init__(self, asteroidfield):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.score = 0
        self.asteroidfield = asteroidfield
        self.time = 0

    def update(self, dt):
        self.score += (SCORE_MAX_PER_SECOND * dt *
                       self.asteroidfield.density / ASTERIOD_MAX_DENSITY)
        self.time += dt

    def count_split(self):
        self.score += SCORE_PER_SPLIT
