import pygame
import random
from asteroids import Asteroid
from constants import (
    ASTEROID_MAX_RADIUS,
    ASTERIOD_MAX_DENSITY,
    ASTEROID_KINDS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPAWN_RATE_SECONDS,
    BACKGROUND_VELOCITY,
    BACKGROUND_ROTATION_NEW_SECONDS,
)
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
        self.BACKGROUND_IMG = pygame.image.load("assets/background_2.jpg").convert()
        self.background_section = self.rect.copy()
        self.background_section.move_ip(pygame.Vector2(
            self.BACKGROUND_IMG.get_rect().center))
        self.rotation_old = random.uniform(0, 360)
        self.rotation = self.rotation_old
        self.rotation_new = random.uniform(0, 360)
        self.rotation_timer = BACKGROUND_ROTATION_NEW_SECONDS
        self.background_movement = pygame.Vector2(0, 0)

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
        self.update_rotation(dt)
        self.move_background(dt)

    def calc_asteroid_density(self):
        rect_area = self.rect.width * self.rect.height
        asteroid_area = 0
        for asteroid in self.asteroids_group:
            asteroid_area += 3.14 * asteroid.radius ** 2
        return asteroid_area / rect_area

    def draw_background(self, surf):
        surf.blit(self.BACKGROUND_IMG, self.rect, self.background_section)

    def move_background(self, dt):
        # sum up movement until long enough
        self.background_movement += pygame.Vector2(1, 0).rotate(
            self.rotation) * BACKGROUND_VELOCITY * dt

        # do not move if less than 1 pixel
        if self.background_movement.length() < 1:
            return

        background_rect = self.BACKGROUND_IMG.get_rect()
        self.background_section = self.move_rect_and_keep_in_rect(
            self.background_section, background_rect, self.background_movement)
        self.background_movement = pygame.Vector2(0, 0)

    def update_rotation(self, dt):
        self.rotation_timer -= dt
        if self.rotation_timer <= 0:
            self.rotation_timer = BACKGROUND_ROTATION_NEW_SECONDS
            self.rotation_old = self.rotation_new
            self.rotation_new = random.uniform(0, 360)

        normalized = self.rotation_timer / BACKGROUND_ROTATION_NEW_SECONDS
        self.rotation = normalized * self.rotation_old + \
            (1 - normalized) * self.rotation_new

    def move_rect_and_keep_in_rect(self, inner_rect, outer_rect, move_vector):
        moved_rect = inner_rect.move(move_vector)
        if moved_rect.left <= outer_rect.left:
            print("left border")
            reflected_vector = move_vector.reflect(
                pygame.Vector2(1, 0)) + pygame.Vector2(1, 0)
            self.add_to_rotation_and_reset_timer(move_vector.angle_to(reflected_vector))
            moved_rect = inner_rect.move(reflected_vector)
        if moved_rect.right >= outer_rect.right:
            print("right border")
            reflected_vector = move_vector.reflect(
                pygame.Vector2(-1, 0)) + pygame.Vector2(-1, 0)
            self.add_to_rotation_and_reset_timer(move_vector.angle_to(reflected_vector))
            moved_rect = inner_rect.move(reflected_vector)
        if moved_rect.top <= outer_rect.top:
            print("top border")
            reflected_vector = move_vector.reflect(
                pygame.Vector2(0, 1)) + pygame.Vector2(0, 1)
            self.add_to_rotation_and_reset_timer(move_vector.angle_to(reflected_vector))
            moved_rect = inner_rect.move(reflected_vector)
        if moved_rect.bottom >= outer_rect.bottom:
            print("bottom border")
            reflected_vector = move_vector.reflect(
                pygame.Vector2(0, -1)) + pygame.Vector2(0, -1)
            self.add_to_rotation_and_reset_timer(move_vector.angle_to(reflected_vector))
            moved_rect = inner_rect.move(reflected_vector)
        return moved_rect

    def add_to_rotation_and_reset_timer(self, angle):
        self.rotation += angle
        self.rotation_old = self.rotation
        self.rotation_timer = BACKGROUND_ROTATION_NEW_SECONDS
        self.rotation_new = random.uniform(0, 360)
