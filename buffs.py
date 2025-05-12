import pygame
import random
from circleshape import CircleShape

class Buff(CircleShape):
    containers = None
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Buffs are spawned with a random type. Color is based on type.
        self.type = random.choice(["speed", "fire rate"])
        self.radius = radius
        if self.type == "speed":
            self.color = (0, 255, 0)
        elif self.type == "fire rate":
            self.color = (255, 0, 0)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        return
    
    def update(self, dt):
        self.position += self.velocity * dt
        return