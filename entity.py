
import math
from math import atan2, sin, cos, sqrt, degrees

import pygame
from pygame.locals import *

""" Base Class upon which the rest of the ingame objects are based. Contains
    all of the basic methods needed to be displayed on screen, as well as all 
    of the basic physics methods to drive movement. """
class Entity:
    GRAV = 1.00
    """ loc & vel are both [float; 2].
        radius & rotation are both float
        img is a pygame.image.Surface """
    def __init__(self, loc, vel, radius, rotation, img):
        self.loc = loc   # list of two floating points (x, y)
        self.vel = vel   # list of two floating points (x, y)
        # force is used to determine how to update velocity
        self.force = [0.0, 0.0] # This is determined by the environment
        self.radius = radius
        self.rotation = rotation
        self.image = img

    """ Returns the euclidean distance to the given body, as a float. """
    def distance_to(self, body):
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

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

    def delta_velocity(self, body):
        vx = body.vel[0] - self.vel[0]
        vy = body.vel[1] - self.vel[1]

        return [vx, vy]

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

    """ Resets the Entity's force vector to zero. """
    def clear_force(self):
        self.force = [0.0, 0.0]

    """ Iterates through a list of stars, calculating the gravitaional force
        from each. Updates the Entity's force variable as the summation of
        each calculated force. """
    def iterate_force(self, star_list):
        star_force = [0.0, 0.0] # Reset the entities force value
        for body in star_list:
            d = self.distance_to_squared(body)
            if d != 0:  # Avoid division by zero!!
                r = self.delta_location(body)
                radians = atan2(r[1], r[0])   # Direction
                magnitude = body.mass / d    # Magnitude
                star_force[0] += magnitude * cos(radians)
                star_force[1] += magnitude * sin(radians)
        self.force[0] += star_force[0]
        self.force[1] += star_force[1]

    """ Calculates the velocity needed to orbit the given body with an 
        eccentricity close to zero. """
    def get_orbital_velocity(self, body):
        # Equation for mean orbital speed
        speed = sqrt( (Entity.GRAV * body.mass) / self.distance_to(body) )
        delta = self.delta_location(body)
        angle = atan2(delta[1], delta[0]) + (3.14 / 2.0) # angular offset
        return [
                speed * cos(angle),
                speed * sin(angle),
               ]

    """ Modifies the Entity's rotation such that it points towards the given
        body. """
    def look_at(self, body):
        delta = self.delta_location(body)
        self.rotation = atan2(delta[1], delta[0])

    """ Given a window to draw on, this method internally rotates, scales and
        moves the Entity's image field, then paints it onto the window. 
        Entity's image is scaled such that it's width is equal to the Entity's
        radius.  """
    def draw(self, window):
        image_loc = self.image.get_rect().width
        s = self.radius / self.image.get_rect().width
        # Re-Transform the image for each frame
        transform = pygame.transform.rotozoom(self.image,
                                              degrees(-self.rotation) - 90,
                                              s)
        image_loc = transform.get_rect()
        # Offset the image so that it is centered at the objects location
        offset = [
                  self.loc[0] - image_loc.width/2.0,
                  self.loc[1] - image_loc.height/2.0,
                 ]
        image_loc = image_loc.move(offset)
        # Maybe add guards to check if image is outisde the window?
        window.blit(transform, image_loc)

""" Extension of the Entity class. Used as the basic agents of the game. """
class Enemy(Entity):
    def __init__(self, loc, vel, radius, rotation, booster_speed, health, img):
        Entity.__init__(self, loc, vel, radius, rotation, img)
        self.booster_speed = booster_speed
        self.booster_on = False
        self.is_alive = True
        self.health = health

    """ Decrement the Enemy's health. """
    def harm(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False

    """ Add the force of the Enemy's booster if it is active. """
    def use_booster(self, star_list):
        if self.booster_on:
            self.force[0] += self.booster_speed * cos(self.rotation)
            self.force[1] += self.booster_speed * sin(self.rotation)

    def shoot(self, ent_list, damage, speed):
        proj = Projectile(self, speed, damage, 10, self.image)
        ent_list.append(proj)

class Player(Enemy):
    def __init__(self, weapons):
        weapons = weapons # Is a list of weapons

class Projectile(Entity):
    def __init__(self, body, speed, damage, duration, img):
        self.loc = body.loc
        self.vel = body.vel
        self.force = [0.0, 0.0]
        self.radius = 10.0
        self.rotation = body.rotation
        self.image = img
        self.speed = speed
        self.damage = damage
        self.duration = duration
        # Owner # How would this get implemented?
        self.vel[0] += speed * cos(self.rotation)
        self.vel[1] += speed * sin(self.rotation)

# class Guided(Projectile):

class Star(Entity):
    def __init__(self, loc, vel, radius, mass, img_path):
        Entity.__init__(self, loc, vel, radius, 0, img_path)
        self.rotation = -3.14/2.0 # Hack to make sure that Star object's
        self.mass = 100           # image renders correctly

