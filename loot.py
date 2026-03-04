import random

import pygame

from annotation import Annotation
from circleshape import CircleShape
from constants import LINE_WIDTH, LOOT_ANNOTATION_SECONDS, LOOT_RADIUS


class Loot(CircleShape):
    loot_table = {
        "ore": {
            "chance": 0.2,
            "color": "orange",
            "pickup_action": "loot_ore",
            "destroyable": True,
            "duration": 2,
        },
        "shield": {
            "chance": 0.05,
            "color": "blue",
            "pickup_action": "loot_shield",
            "destroyable": False,
            "duration": 20,
        },
    }

    def __init__(self, x, y, radius, rect):
        super().__init__(x, y, radius, rect)
        self.type = self.roll_type()
        self.color = self.loot_table[self.type]["color"]
        self.pickup_action = self.loot_table[self.type]["pickup_action"]
        self.destroyable = self.loot_table[self.type]["destroyable"]

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, self.position, LOOT_RADIUS, 2 * LINE_WIDTH
        )

    def update(self, dt):
        self.move(dt)
        self.wrap_active_rect()

    def roll_type(self):
        items = list(self.loot_table.keys())
        chances = [loot_type["chance"] for loot_type in self.loot_table.values()]
        return random.choices(items, weights=chances)[0]

    def loot_ore(self, target):
        target.stats.add_ore()
        Annotation(
            target.position.x,
            target.position.y,
            "+1",
            self.color,
            LOOT_ANNOTATION_SECONDS,
        )

    def loot_shield(self, target):
        pass
