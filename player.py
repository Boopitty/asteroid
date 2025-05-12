import pygame
from circleshape import CircleShape
from bullets import Bullet
from constants import PLAYER_RADIUS, PLAYER_TURNING_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED

# The player will look like a triangle but actually be a circle
class Player(CircleShape):    
    # allow the player to be added to groups
    containers = None

    # initialize using the parent class
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0

        # IMPORTANT: VARIABLE NAME CONVENTION:
        # buff names MUST match with the names of
        # the buff types in the Buff class
        self.buffs = {
            "speed": {"active": False, "duration": 14, "timer": 0},
            "fire rate": {"active": False, "duration": 7, "timer": 0},
        }

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
        if self.buffs["speed"]["active"] == False:
            self.rotation += PLAYER_TURNING_SPEED * dt
        else: 
            self.rotation += PLAYER_TURNING_SPEED * 1.5 * dt
        return
    
    # move the player
    def move(self, dt):
        # make a vector in the direction the player is facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # move the player in that direction
        if self.buffs["speed"]["active"] == False:
            self.position += forward * PLAYER_SPEED * dt
        else:
            self.position += forward * PLAYER_SPEED * 1.5 * dt
        return
    
    def activate_buff(self, buff_name):
        # apply buff and set a timer
        self.buffs[buff_name]["active"] = True
        self.buffs[buff_name]["timer"] = self.buffs[buff_name]["duration"]
        return
    
    # check if the given buff timer is over
    
    def check_timer(self, buff_name, dt):
        # decrement the timer
        self.buffs[buff_name]["timer"] -= dt

        # deactivate buff if time's up and reset the timer
        if self.buffs[buff_name]["timer"] <= 0:
            self.buffs[buff_name]["timer"] = 0
            self.buffs[buff_name]["active"] = False

    # update the player position and rotation
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update the cooldown and buff timers
        self.shoot_cooldown -= dt

        # check the buff timers
        for buff_name in self.buffs:
            self.check_timer(buff_name, dt)

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
        if self.buffs["fire rate"]["active"] == False:
            self.shoot_cooldown = .3
        else:
            self.shoot_cooldown = .1
        return