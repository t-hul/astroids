import pygame

from constants import ANNOTATION_FONT_SIZE


class Annotation(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, life_time):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.text = text
        self.color = color
        self.life_time = life_time
        self.font = pygame.font.Font(None, ANNOTATION_FONT_SIZE)

    def draw(self, screen):
        rendered_text = self.font.render(self.text, False, self.color)
        # score_height = score_text.get_height()
        # score_width = score_text.get_width()
        screen.blit(rendered_text, self.position)

    def update(self, dt):
        self.life_time -= dt
        if self.life_time < 0:
            self.kill()
