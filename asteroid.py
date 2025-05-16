import pygame
import random
from player import Player
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    containers = None
    slowed = False
    color = (255, 255, 255)
    modifier = 1.0

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt * self.modifier
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            # spawn two smaller asteroids
            # get a random number for the anlge,
            # then rotate the original vector by that angle
            angle = random.uniform(20, 50)
            velocity1 = self.velocity.rotate(angle)
            velocity2 = self.velocity.rotate(-angle)
            # get new radius and create two new asteroids
            # then set their velocity and speed them up
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = velocity1 * 1.2
            asteroid2.velocity = velocity2 * 1.2