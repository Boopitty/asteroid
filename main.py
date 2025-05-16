# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
# import constants from the constants.py file
from constants import *
pygame.init
from player import Player
from bullets import Bullet
from asteroid import Asteroid
from buffs import Buff, Effects
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
buffs = pygame.sprite.Group()

# add classes to the groups
Player.containers = (updatable, drawable)
Asteroid.containers = (updatable, drawable, asteroids)
AsteroidField.containers = (updatable)
Bullet.containers = (updatable, drawable, bullets)
Buff.containers = (updatable, drawable, buffs)

# create a player object and an asteroid field object
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
feild = AsteroidField()
score = 0

# main loop. this is where the game will run
while True:
    # enable the user to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # fill the screen with black        
    pygame.Surface.fill(screen, color = (0,0,0))

    # Set the frame rate to 60 FPS and set dt variable
    # Delta time = seconds since last frame(/1000 turns miliseconds to seconds)
    # sets time between frames to 1/60 of a second
    dt = clock.tick(60) / 1000

    # update all the sprites in the updatable group
    updatable.update(dt)

    if player.effects.is_active("slow"):
        Asteroid.color = (255, 0, 255)
        Asteroid.modifier = player.effects.get_modifier("slow")
    else:
        Asteroid.color = (255, 255, 255)
        Asteroid.modifier = 1.0

    # check each asteroid for collisions with the player
    for asteroid in asteroids:

        if player.collide(asteroid):
            if player.effects.is_active("shield"):
                asteroid.kill()
                player.effects.deactivate_buff("shield")
            else:
                survived = pygame.time.get_ticks() # milliseconds
                print("Game Over!")
                print(f"Asteroids Destroyed: {score}")
                # (full seconds).(remaninder of seconds converted to tenths of a second)
                print(f"Time Survived: {survived // 1000}.{(survived % 1000) // 100}")
                pygame.quit()
                exit()

        for bullet in bullets:
            if asteroid.collide(bullet):
                bullet.kill()
                asteroid.split()
                score += 1
        
    for buff in buffs:
        if player.collide(buff):
            buff.kill()
            player.effects.activate_buff(buff.type)

    for sprite in drawable:
        sprite.draw(screen)

    # update the display
    pygame.display.flip()

if __name__ == "__main__":
    main()