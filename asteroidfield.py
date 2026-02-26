import pygame
import random
from asteroids import Asteroid
from constants import (ASTEROID_MAX_RADIUS, ASTERIOD_MAX_DENSITY,
                       ASTEROID_SPAWN_RATE_SECONDS, ASTEROID_KINDS, ASTEROID_MIN_RADIUS)
from logger import log_event


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, asteroids_group):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

        self.rect = pygame.Rect(left, top, width, height)
        self.edges = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(left - ASTEROID_MAX_RADIUS, top + y * height),
            ],
            [
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(
                    left + width + ASTEROID_MAX_RADIUS, top + y * height),
            ],
            [
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(left + x * width, top - ASTEROID_MAX_RADIUS),
            ],
            [
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(
                    left + x * width, top + height + ASTEROID_MAX_RADIUS),
            ],
        ]
        self.asteroids_group = asteroids_group
        self.density = 0

    def spawn(self, radius, position, velocity):
        if self.density > ASTERIOD_MAX_DENSITY:
            log_event("max_density", density=self.density)
            return
        asteroid = Asteroid(position.x, position.y, radius, self.rect)
        asteroid.velocity = velocity
        log_event("asteroid_spawned", density=self.density)

    def update(self, dt):
        self.density = self.calc_asteroid_density()
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def calc_asteroid_density(self):
        rect_area = self.rect.width * self.rect.height
        asteroid_area = 0
        for asteroid in self.asteroids_group:
            asteroid_area += 3.14 * asteroid.radius ** 2
        return asteroid_area / rect_area
