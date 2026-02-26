import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, rect):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.active_rect = rect

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def move(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

    def wrap_active_rect(self):
        if self.position.x > self.active_rect.right + self.radius:
            self.position.x = self.active_rect.left - self.radius
        if self.position.x < self.active_rect.left - self.radius:
            self.position.x = self.active_rect.right + self.radius
        if self.position.y > self.active_rect.bottom + self.radius:
            self.position.y = self.active_rect.top - self.radius
        if self.position.y < self.active_rect.top - self.radius:
            self.position.y = self.active_rect.bottom + self.radius
