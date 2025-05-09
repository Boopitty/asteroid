import pygame
from circleshape import CircleShape

class Bullet(CircleShape):
    containers = None
    def __init__(self, x, y):
        super().__init__(x, y, 5)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)
        return
    
    def update(self, dt):
        self.position += self.velocity * dt
        return