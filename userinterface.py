import pygame

from constants import PLAYER_LIVES, SCREEN_WIDTH, UI_FONT_SIZE, UI_TOP_HEIGHT


class UserInterface(pygame.sprite.Sprite):
    def __init__(self, score, player):
        self.score = score
        self.player = player
        self.top_bar = pygame.Rect(0, 0, SCREEN_WIDTH, UI_TOP_HEIGHT)
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.heart_life_img = pygame.image.load(
            "assets/heart_32x32.png"
        ).convert_alpha()
        self.heart_dead_img = pygame.image.load(
            "assets/heart_dead_32x32.png"
        ).convert_alpha()

    def draw(self, screen):
        pygame.draw.rect(screen, "gray", self.top_bar)
        score_text = self.font.render(
            f"{int(self.score.float_value)}", True, "black", "gray"
        )
        score_height = score_text.get_height()
        score_width = score_text.get_width()
        screen.blit(
            score_text,
            (SCREEN_WIDTH - score_width - 10, (UI_TOP_HEIGHT - score_height) / 2),
        )

        for i in range(PLAYER_LIVES):
            x_pos = SCREEN_WIDTH / 2 + (i - PLAYER_LIVES / 2) * 40
            y_pos = UI_TOP_HEIGHT / 2 - 16
            if i < PLAYER_LIVES - self.player.lives:
                screen.blit(self.heart_dead_img, (x_pos, y_pos))
            else:
                screen.blit(self.heart_life_img, (x_pos, y_pos))
