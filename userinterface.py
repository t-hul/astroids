import pygame
from constants import SCREEN_WIDTH, UI_TOP_HEIGHT, UI_FONT_SIZE


class UserInterface(pygame.sprite.Sprite):
    def __init__(self, score):
        self.score = score
        self.top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, UI_TOP_HEIGHT)
        self.font = pygame.font.Font(None, UI_FONT_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, "gray", self.top_bar)
        score_text = self.font.render(
            f"{int(self.score.float_value)}", True, "black", "gray")
        score_height = score_text.get_height()
        score_width = score_text.get_width()
        screen.blit(score_text, (SCREEN_WIDTH - score_width -
                    10, (UI_TOP_HEIGHT-score_height)/2))
