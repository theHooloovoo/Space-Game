
import math
from math import atan2, sin, cos

import pygame
from pygame.locals import *

""" Base Class upon which the rest of the ingame objects are based. Contains
    all of the basic methods needed to be displayed on screen, as well as all 
    of the basic physics methods to drive movement. """
class Entity:
    def __init__(self, loc, vel, radius, rotation, img_path):
        self.loc = loc   # list of two floating points (x, y)
        self.vel = vel   # list of two floating points (x, y)
        self.force = [0.0, 0.0] # This is determined by the environment
        self.radius = radius
        self.rotation = rotation
        self.image = pygame.image.load(img_path)

    """ Returns the euclidean distance to the given body, as a float. """
    def distance_to(self, x, y):
        dx = x - self.loc[0]
        dy = y - self.loc[1]

        return sqrt(dx*dx + dy*dy)

    """ Same as the 'distance_to()' method, but doesn't square root the
        answer. """
    def distance_to_squared(self, body):
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

        return dx*dx + dy*dy

    """ Returns the difference in x and y coordinates from the given body, as
        a list of floats. """
    def delta_location(self, body):
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

        return [dx, dy]

    """ Returns True if self and body are touching. Collision detection upon
        two circles. """
    def touching(self, body):
        d = self.distance_to(body)
        if d <= self.radius + body.radius:
            return True
        else:
            return False

    """ Increments the Entity's location by the Entities experienced
        velocity. """
    def iterate_location(self, dt):
        self.loc[0] += self.vel[0] * dt
        self.loc[1] += self.vel[1] * dt

    """ Increments the Entity's velocity by the Entities experienced force. """
    def iterate_velocity(self, dt):
        self.vel[0] += self.force[0] * dt
        self.vel[1] += self.force[1] * dt

    """ Iterates through a list of stars, calculating the gravitaional force
        from each. Updates the Entity's force variable as the summation of
        each calculated force. """
    def iterate_force(self, star_list):
        resultant_force = [0.0, 0.0] # Reset the entities force value
        for body in star_list:
            d = self.distance_to_squared(body)
            if d != 0:  # Avoid division by zero!!
                r = self.delta_location(body)
                radians = atan2(r[1], r[0])   # Direction
                magnitude = body.mass / d    # Magnitude
                resultant_force[0] += magnitude * cos(radians) * 10
                resultant_force[1] += magnitude * sin(radians) * 10
        self.force = resultant_force

    """ Given a window to draw on, this methods internally rotates, scales and
        moves the Entity's image field, then paints it onto the window. 
        Entity's image is scaled such that it's width is equal to the Entity's
        radius.  """
    def draw(self, window):
        image_loc = self.image.get_rect().width
        s = self.radius / self.image.get_rect().width
        # Re-Transform the image for each frame
        transform = pygame.transform.rotozoom(self.image, self.rotation, s)
        image_loc = transform.get_rect()
        # Offset the image so that it is centered at the objects location
        offset = [
                  self.loc[0] - image_loc.width/2.0,
                  self.loc[1] - image_loc.height/2.0,
                 ]
        image_loc = image_loc.move(offset)
        # Maybe add guards to check if image is outisde the window?
        window.blit(transform, image_loc)

class Enemy(Entity):
    def __init__(self, loc, vel, radius, rotation, booster_speed, health):
        Entity.__init__(self, loc, vel, radius, rotation, img_path)
        self.booster_speed = booster_speed
        self.health = health

class Player(Enemy):
    def __init__(self, weapons):
        weapons = weapons # Is a list of weapons

class Projectile(Entity):
    def __init__(self, speed, damage, duration):
        # Entity.__init__(self, <-- Finish!!
        self.speed = speed
        self.damage = damage
        self.duration = duration
        # Owner # How would this get implemented?

# class Guided(Projectile):

class Star(Entity):
    def __init__(self, loc, vel, radius, mass, img_path):
        Entity.__init__(self, loc, vel, radius, 0, img_path)
        self.mass = 100

