import pygame
import random
from asteroid import Asteroid
from buffs import Buff
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    containers = None
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.asteroid_spawn_timer = 0.0
        self.buff_spawn_timer = 0.0

    def spawn_asteroid(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
    
    def spawn_buff(self, position, velocity):
        buff = Buff(position.x, position.y, ASTEROID_MIN_RADIUS)
        buff.velocity = velocity

    def update(self, dt):
        self.asteroid_spawn_timer += dt
        self.buff_spawn_timer += dt

        if self.asteroid_spawn_timer > ASTEROID_SPAWN_RATE:
            self.asteroid_spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn_asteroid(ASTEROID_MIN_RADIUS * kind, position, velocity)
        
        if self.buff_spawn_timer > BUFF_SPAWN_RATE:
            self.buff_spawn_timer = 0

            # spawn a new buff
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            self.spawn_buff(position, velocity)