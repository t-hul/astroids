import sys

import pygame

from asteroidfield import AsteroidField
from asteroids import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, UI_TOP_HEIGHT
from logger import log_event, log_state
from player import Player
from stats import Stats
from shot import Shot
from userinterface import UserInterface


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    Stats.containers = updatable
    asteroidfield = AsteroidField(
        0, UI_TOP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - UI_TOP_HEIGHT, asteroids)
    player = Player(asteroidfield.rect)
    stats = Stats(asteroidfield)
    ui = UserInterface(stats, player)

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        asteroidfield.draw_background(screen)

        updatable.update(dt)
        for item in drawable:
            item.draw(screen)
        ui.draw(screen)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                player.loose_life()
                if player.lifes <= 0:
                    print("Game over!")
                    print(f"Score: {int(stats.score)}")
                    sys.exit()
                for asteroid in asteroids:
                    asteroid.kill()
                asteroids.clear(screen, asteroidfield.draw_background(screen))
                player.reset(screen)
                ui.draw(screen)
                pygame.display.flip()
                pygame.time.wait(500)

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.take_damage(shot.damage, stats)
                    shot.kill()

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
