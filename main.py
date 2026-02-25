import sys

import pygame

from asteroidfield import AsteroidField
from asteroids import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, UI_TOP_HEIGHT
from logger import log_event, log_state
from player import Player
from score import Score
from shot import Shot
from userinterface import UserInterface


def clear_screen(surf, rect):
    surf.fill("black", rect)


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    playground = pygame.Rect(
        0, UI_TOP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - UI_TOP_HEIGHT
    )
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Score.containers = updatable
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    score = Score()
    ui = UserInterface(score, player)

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        updatable.update(dt)
        for item in drawable:
            item.draw(screen)
        ui.draw(screen)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                player.loose_live()
                if player.lives <= 0:
                    print("Game over!")
                    print(f"Score: {int(score.float_value)}")
                    sys.exit()
                for asteroid in asteroids:
                    asteroid.kill()
                asteroids.clear(screen, clear_screen(screen, playground))
                player.reset(screen)
                ui.draw(screen)
                pygame.display.flip()
                pygame.time.wait(500)

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score.count_split()

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
