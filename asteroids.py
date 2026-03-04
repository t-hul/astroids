import random

import pygame

from annotation import Annotation
from circleshape import CircleShape
from constants import (
    ASTEROID_MIN_HEALTH,
    ASTEROID_MIN_RADIUS,
    DAMAGE_ANNOTATION_SECONDS,
    LINE_WIDTH,
    LOOT_RADIUS,
)
from logger import log_event
from loot import Loot


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, rect):
        super().__init__(x, y, radius, rect)
        self.area = 3.14 * self.radius**2
        self.start_health = (
            self.area * ASTEROID_MIN_HEALTH / (3.14 * ASTEROID_MIN_RADIUS**2)
        )
        self.health = self.start_health

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.move(dt)
        self.wrap_active_rect()

    def split(self, stats):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        first_split_velocity = self.velocity.rotate(random_angle)
        second_split_velocity = self.velocity.rotate(-random_angle)
        split_radius = self.radius - ASTEROID_MIN_RADIUS

        first_split_asteroid = Asteroid(
            self.position.x, self.position.y, split_radius, self.active_rect
        )
        first_split_asteroid.velocity = first_split_velocity * 1.2
        second_split_asteroid = Asteroid(
            self.position.x, self.position.y, split_radius, self.active_rect
        )
        second_split_asteroid.velocity = second_split_velocity * 1.2
        self.spawn_loot()

        stats.count_split(self.start_health)

    def take_damage(self, damage, stats):
        self.health -= damage
        Annotation(
            self.position.x,
            self.position.y,
            f"-{damage}",
            "red",
            DAMAGE_ANNOTATION_SECONDS,
        )
        if self.health <= 0:
            self.split(stats)

    def spawn_loot(self):
        new_loot = Loot(self.position.x, self.position.y, LOOT_RADIUS, self.active_rect)
        new_loot.velocity = self.velocity
