import pygame

from constants import PLAYER_LIFES, SCREEN_WIDTH, UI_FONT_SIZE, UI_TOP_HEIGHT


class UserInterface(pygame.sprite.Sprite):
    def __init__(self, stats, player):
        self.stats = stats
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
        self.draw_score(screen)
        self.draw_lifes(screen)
        self.draw_time(screen)

    def draw_score(self, screen):
        score_text = self.font.render(
            f"{int(self.stats.score)}", True, "black", "gray"
        )
        score_height = score_text.get_height()
        score_width = score_text.get_width()
        screen.blit(
            score_text,
            (SCREEN_WIDTH - score_width - 10, (UI_TOP_HEIGHT - score_height) / 2),
        )

    def draw_lifes(self, screen):
        for i in range(PLAYER_LIFES):
            x_pos = SCREEN_WIDTH / 2 + (i - PLAYER_LIFES / 2) * 40
            y_pos = UI_TOP_HEIGHT / 2 - 16
            if i < PLAYER_LIFES - self.player.lifes:
                screen.blit(self.heart_dead_img, (x_pos, y_pos))
            else:
                screen.blit(self.heart_life_img, (x_pos, y_pos))

    def draw_time(self, screen):
        time = int(self.stats.time)
        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = (time % 3600) % 60
        time_text = self.font.render(
            f"{hours:02}:{minutes:02}:{seconds:02}", True, "black", "gray"
        )
        height = time_text.get_height()
        screen.blit(
            time_text,
            (10, (UI_TOP_HEIGHT - height) / 2),
        )
