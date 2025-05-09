# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
# import constants from the constants.py file
from constants import *
pygame.init
from player import Player, Bullet
from asteroid import Asteroid
from asteroidfield import AsteroidField

# create a screen object and print the screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
print("Starting Asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

# create a clock object to control the frame rate
clock = pygame.time.Clock()
dt = 0

# Create groups for sprites
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# add classes to the groups
Player.containers = (updatable, drawable)
Asteroid.containers = (updatable, drawable, asteroids)
AsteroidField.containers = (updatable)
Bullet.containers = (updatable, drawable, bullets)


# create a player object
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
feild = AsteroidField()
# main loop. this is where the game will run
while True:
    # enable the user to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # fill the screen with black        
    pygame.Surface.fill(screen, color = (0,0,0))

    # update all the sprites in the updatable group
    updatable.update(dt)
    for sprite in asteroids:
        # check for collisions with the player
        if player.collide(sprite):
            print("Game Over!")
            pygame.quit()
            exit()
        for bullet in bullets:
            if sprite.collide(bullet):
                bullet.kill()
                sprite.split()

    # iterate over drawable group and draw each sprite
    for sprite in drawable:
        sprite.draw(screen)

    # update the display
    pygame.display.flip()

    # Set the frame rate to 60 FPS and set dt variable
    # Delta time = seconds since last frame(/1000 turns miliseconds to seconds)
    dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()