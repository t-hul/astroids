import pygame
from constants import SCORE_PER_SECOND


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.float_value = 0

    def update(self, dt):
        self.float_value += SCORE_PER_SECOND * dt
