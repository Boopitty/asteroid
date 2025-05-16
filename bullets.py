import pygame
from circleshape import CircleShape

class Bullet(CircleShape):
    containers = None
    def __init__(self, x, y, color):
        super().__init__(x, y, 5)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
    
    def update(self, dt):
        self.position += self.velocity * dt