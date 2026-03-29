import pygame

from animation import Animation
from circleshape import CircleShape
from constants import (
    BOOST_ENERGY_COST_PER_SECOND,
    BOOST_MULTIPLIER,
    LINE_WIDTH,
    PLAYER_ACCELERATION,
    PLAYER_LIFES,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_SHIELD_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOT_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_ENERGY_COST_PER_SECOND,
    TOGGLE_DEBOUNCE_SECONDS,
)
from logger import log_event
from shot import Shot


class Player(CircleShape):
    def __init__(self, rect, stats):
        super().__init__(*rect.center, PLAYER_RADIUS, rect)
        self.rotation = 180
        self.speed = 0
        self.shot_timer = 0
        self.lifes = PLAYER_LIFES
        self.color = "white"
        self.stats = stats
        self.is_boosting = False
        self.has_shield = False
        self.toggle_shield_timer = 0
        self.thruster_animation = Animation(
            "assets/thruster_flame_sprite_sheet.png", self, 16, 16, (1, 0.5)
        )

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), LINE_WIDTH)
        if self.has_shield:
            pygame.draw.circle(
                screen,
                "blue",
                self.position,
                PLAYER_SHIELD_RADIUS,
                LINE_WIDTH,
            )

    def rotate(self, dt):
        if self.is_boosting:
            return
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        # self.speed = min(PLAYER_SPEED, self.speed + PLAYER_ACCELERATION * dt)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.get_acceleration() * dt
        self.velocity += rotated_with_speed_vector
        # if self.velocity.length() > self.get_max_speed():
        #     self.velocity.scale_to_length(self.get_max_speed())
        self.velocity.clamp_magnitude_ip(self.get_max_speed())

    def boost(self, dt):
        if self.stats.energy <= 0:
            return
        self.is_boosting = True
        self.accelerate(dt)
        self.stats.energy -= BOOST_ENERGY_COST_PER_SECOND * dt

    def get_max_speed(self):
        return (
            BOOST_MULTIPLIER * PLAYER_MAX_SPEED
            if self.is_boosting
            else PLAYER_MAX_SPEED
        )

    def get_acceleration(self):
        return (
            BOOST_MULTIPLIER * PLAYER_ACCELERATION
            if self.is_boosting
            else PLAYER_ACCELERATION
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_timer -= dt
        self.toggle_shield_timer -= dt
        if self.has_shield:
            self.stats.energy -= SHIELD_ENERGY_COST_PER_SECOND * dt
            if self.stats.energy <= 0:
                self.stats.energy = 0
                self.has_shield = False

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_LSHIFT]:
            self.boost(dt)
        if not keys[pygame.K_LSHIFT] and self.is_boosting:
            self.is_boosting = False
        if keys[pygame.K_f]:
            self.toggle_shield()

        self.move(dt)
        self.wrap_active_rect()

    def collides_with(self, other):
        if self.has_shield:
            return False
        # approximate trinagle by corner points and midpoints
        # test if any point is inside other
        corners = self.triangle()
        points_to_test = corners.copy()
        for i in range(len(corners)):
            midpoint = corners[i].lerp(corners[(i + 1) % len(corners)], 0.5)
            points_to_test.append(midpoint)

        for point in points_to_test:
            distance = point.distance_to(other.position)
            if distance <= other.radius:
                return True
        return False

    def shoot(self):
        if self.shot_timer > 0:
            return
        self.shot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        front_position = self.triangle()[0]
        shot = Shot(front_position.x, front_position.y, self.active_rect)
        shot.velocity = (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            + self.velocity
        )

    def lose_life(self):
        self.lifes -= 1
        print(f"You are hit! {self.lifes}/{PLAYER_LIFES} lifes left")
        log_event("player_hit")

    def reset(self, screen):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.draw(screen)

    def pickup(self, loot_item):
        self.color = loot_item.color
        action = loot_item.pickup_action
        if hasattr(loot_item, action):
            getattr(loot_item, action)(self)
        else:
            raise NotImplementedError(f"Action '{action}' is not implemented")

    def toggle_shield(self):
        if self.stats.energy <= 0 and not self.has_shield:
            return
        if self.toggle_shield_timer > 0:
            return
        self.toggle_shield_timer = TOGGLE_DEBOUNCE_SECONDS
        if self.has_shield:
            self.has_shield = False
        else:
            self.has_shield = True
