import pygame
from constants import SCORE_MAX_PER_SECOND, SCORE_PER_SPLIT, ASTERIOD_MAX_DENSITY


class Score(pygame.sprite.Sprite):
    def __init__(self, asteroidfield):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.float_value = 0
        self.asteroidfield = asteroidfield

    def update(self, dt):
        self.float_value += (SCORE_MAX_PER_SECOND * dt *
                             self.asteroidfield.density / ASTERIOD_MAX_DENSITY)

    def count_split(self):
        self.float_value += SCORE_PER_SPLIT
