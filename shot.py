from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH
import pygame


class Shot(CircleShape):
    def __init__(self, x, y, rect):
        super().__init__(x, y, SHOT_RADIUS, rect)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.move(dt)
