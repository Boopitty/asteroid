import pygame
from circleshape import CircleShape
from bullets import Bullet
from buffs import Effects
from constants import PLAYER_RADIUS, PLAYER_TURNING_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED

# The player will look like a triangle but actually be a circle
class Player(CircleShape):    
    # allow the player to be added to groups
    containers = None

    # initialize using the parent class
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.effects = Effects()
        self.rotation = 0
        self.shoot_cooldown = 0

    # triangle method returns the three points of the triangle
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # draw the player as a triangle
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
        return
    
    # rotate the player
    def rotate(self, dt):
        self.rotation += PLAYER_TURNING_SPEED * dt * self.effects.modifier("speed")
    
    # move the player
    def move(self, dt):
        # make a vector in the direction the player is facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # move the player in that direction
        self.position += forward * PLAYER_SPEED * dt * self.effects.modifier("speed")
    
    # update the player position and rotation
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update the cooldown and buff timers
        self.shoot_cooldown -= dt

        if keys[pygame.K_a]:
            # rotate left when a key is pressed
            self.rotate(-dt)
        if keys[pygame.K_d]:
            # rotate right when d key is pressed
            self.rotate(dt)
        if keys[pygame.K_w]:
            # move forward when w key is pressed
            self.move(dt)
        if keys[pygame.K_s]:
            # move backward when s key is pressed
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def shoot(self):
        if self.shoot_cooldown > 0:
            # if the cooldown is not over, do nothing
            return
        # create a new bullet at the player's position
        # and set its velocity to the direction the player is facing
        shot = Bullet(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        # shooting cooldown
        self.shoot_cooldown = .3 * self.effects.modifier("fire rate")