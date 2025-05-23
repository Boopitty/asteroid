import pygame
import random
from circleshape import CircleShape

class Buff(CircleShape):
    containers = None
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        # Buffs are spawned with a random type. Color is based on type.
        self.type = random.choice(["speed", "fire rate", "shield", "slow"])
        self.radius = radius
        if self.type == "speed":
            self.color = (0, 255, 0)
        elif self.type == "fire rate":
            self.color = (255, 0, 0)
        elif self.type == "shield":
            self.color = (0, 0, 255)
        elif self.type == "slow":
            self.color = (255, 0, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
    
class Effects():
    containers = None
    def __init__(self):
        # IMPORTANT: VARIABLE NAME CONVENTION:
        # buff names MUST match with the names of
        # the buff types in the Buff class
        self.buffs = {
            "speed": {"active": False, "duration": 14, "timer": 0, "modifier": 1.5},
            "fire rate": {"active": False, "duration": 7, "timer": 0, "modifier": 0.5},
            "shield": {"active": False, "duration": 10, "timer": 0, "modifier": 1},
            "slow": {"active": False, "duration": 5, "timer": 0, "modifier": 0.5},
        }
    
    def activate_buff(self, buff_name):
        self.buffs[buff_name]["active"] = True
        self.buffs[buff_name]["timer"] = self.buffs[buff_name]["duration"]
    
    def deactivate_buff(self, buff_name):
        self.buffs[buff_name]["active"] = False
        self.buffs[buff_name]["timer"] = 0
      
    def check_timer(self, buff_name, dt):
        self.buffs[buff_name]["timer"] -= dt

        if self.buffs[buff_name]["timer"] <= 0:
            self.deactivate_buff(buff_name)

    def is_active(self, buff_name):
        return self.buffs[buff_name]["active"]

    def get_modifier(self, buff_name):
        if self.buffs[buff_name]["active"]:
            return self.buffs[buff_name]["modifier"]
        else:
            return 1
    
    def update(self, dt):
        # update the timers for all buffs
        for buff_name in self.buffs:
            if self.buffs[buff_name]["active"]:
                self.check_timer(buff_name, dt)