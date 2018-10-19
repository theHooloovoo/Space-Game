
import math
from math import atan2, sin, cos, sqrt, degrees

import random
from random import random

import pygame
from pygame.locals import *

class Entity:
    """ Base Class upon which the rest of the ingame objects are based.
        Contains all of the basic methods needed to be displayed on screen,
        as well as all of the basic physics methods to drive movement.
    """
    GRAV = 30.00
    def __init__(self, loc, vel, radius, rotation, img):
        """ loc & vel are both [float; 2].
            radius & rotation are both float
            img is a pygame.image.Surface
        """
        self.loc = loc   # list of two floating points (x, y)
        self.vel = vel   # list of two floating points (x, y)
        # force is used to determine how to update velocity
        self.force = [0.0, 0.0] # This is determined by the environment
        self.radius = radius
        self.rotation = rotation    # In radians
        self.rot_delta = 0.0        # Rotational speed (also in radius)
        self.image = img

    def distance_to(self, body):
        """ Returns the euclidean distance to the given body, as a float.
        """
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

        return sqrt(dx*dx + dy*dy)

    def distance_to_squared(self, body):
        """ Same as the 'distance_to()' method, but doesn't square root the
            answer.
        """
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

        return dx*dx + dy*dy

    def get_location(self):
        return self.loc

    def delta_location(self, body):
        """ Returns the difference in x and y coordinates from the given
            body, as a list of floats.
        """
        dx = body.loc[0] - self.loc[0]
        dy = body.loc[1] - self.loc[1]

        return [dx, dy]

    def delta_velocity(self, body):
        vx = body.vel[0] - self.vel[0]
        vy = body.vel[1] - self.vel[1]

        return [vx, vy]

    def touching(self, body):
        """ Returns True if self and body are touching. Collision detection
            upon two circles.
        """
        d = self.distance_to(body)
        if d <= self.radius + body.radius:
            return True
        else:
            return False

    def iterate_location(self, dt):
        """ Increments the Entity's location by the Entities experienced
            velocity.
        """
        self.loc[0] += self.vel[0] * dt
        self.loc[1] += self.vel[1] * dt

        self.rotation += self.rot_delta

    def iterate_velocity(self, dt):
        """ Increments the Entity's velocity by the Entities experienced force.
        """
        self.vel[0] += self.force[0] * dt
        self.vel[1] += self.force[1] * dt

    def clear_force(self):
        """ Resets the Entity's force vector to zero.
        """
        self.force = [0.0, 0.0]

    def iterate_force(self, star_list):
        """ Iterates through a list of stars, calculating the gravitaional
            force from each. Updates the Entity's force variable as the
            summation of each calculated force.
        """
        star_force = [0.0, 0.0] # Reset the entities force value
        for body in star_list:
            d = self.distance_to_squared(body)
            if d != 0:  # Avoid division by zero!!
                r = self.delta_location(body)
                radians = atan2(r[1], r[0])   # Direction
                magnitude = Entity.GRAV * body.mass / d    # Magnitude
                star_force[0] += magnitude * cos(radians)
                star_force[1] += magnitude * sin(radians)
        self.force[0] += star_force[0]
        self.force[1] += star_force[1]

    def get_orbital_velocity(self, body, counter_clockwise=True):
        """ Calculates the velocity needed to orbit the given body with an 
            eccentricity close to zero. counter_clockwise is used to set the
            orbital direction.
        """
        # Angular offset, the velocity needs to be tangental to the
        # direction of the attracting body
        offset = 3.14 / 2.0
        if counter_clockwise == False:
            offset = -3.14 / 2.0
        delta = self.delta_location(body)
        # Construct velocity vector
        # Magnitude = Equation for mean orbital speed
        speed = sqrt( (Entity.GRAV * body.mass) / self.distance_to(body) )
        angle = atan2(delta[1], delta[0]) + offset # angular offset
        return [
                speed * cos(angle),
                speed * sin(angle),
               ]

    def look_at(self, body):
        """ Modifies the Entity's rotation such that it points towards the given
            body.
        """
        delta = self.delta_location(body)
        self.rotation = atan2(delta[1], delta[0])

    def point_to(self, loc):
        """ Takes in a list of two floats, then points the Entity towards that
            point.
        """
        delta = [loc[0] - self.loc[0], loc[1] - self.loc[1]]
        self.rotation = atan2(delta[1], delta[0])

    def draw(self, window, cam):
        """ Given a window to draw on, this method internally rotates, scales and
            moves the Entity's image field, then paints it onto the window. 
            Entity's image is scaled such that it's width is equal to the Entity's
            radius. 
        """
        screen_width  = window.get_width()
        screen_height = window.get_height()
        # Get the screen-space for the Entity
        screen_space = cam.get_screen_space(window, self.loc)
        # Scale the image based on the Entity's radius
        image_width = self.image.get_rect().width
        s = self.radius / self.image.get_rect().width
        # Re-Transform the image for each frame
        transform = pygame.transform.rotozoom(self.image,
                                              degrees(-self.rotation) - 90,
                                              s * cam.get_zoom())
        image_loc = transform.get_rect()
        # Offset the image so that it is centered at the objects location
        screen_space[0] -= image_loc.width/2.0
        screen_space[1] -= image_loc.height/2.0
        new_img_loc = image_loc.move(screen_space)
        # Maybe add guards to check if image is outisde the window?
        window.blit(transform, new_img_loc)

    def draw2(self, window, cam, offset):
        """ Given a window to draw on, this method internally rotates, scales and
            moves the Entity's image field, then paints it onto the window. 
            Entity's image is scaled such that it's width is equal to the Entity's
            radius. 
        """
        image_loc = self.image.get_rect().width
        s = self.radius / self.image.get_rect().width
        # Re-Transform the image for each frame
        transform = pygame.transform.rotozoom(self.image,
                                              degrees(-self.rotation) - 90,
                                              s * cam.get_zoom())
        image_loc = transform.get_rect()
        # Offset the image so that it is centered at the objects location
        offset = [
                  self.loc[0] - image_loc.width/2.0,
                  self.loc[1] - image_loc.height/2.0,
                 ]
        image_loc = image_loc.move(offset)
        # Maybe add guards to check if image is outisde the window?
        window.blit(transform, image_loc)

class Agent(Entity):
    """ Extension of the Entity class. Used as the basic agents of the game.
    """
    def __init__(self, loc, vel, radius, rotation, booster_speed, health, img):
        Entity.__init__(self, loc, vel, radius, rotation, img)
        self.booster_speed = booster_speed
        self.booster_on = False
        self.is_alive = True
        self.health = health
        self.image_scrap = img  # Seperate image used for explosion()

    def harm(self, damage):
        """ Decrement the Agent's health.
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False

    def use_booster(self):
        """ Add the force of the Agent's booster if it is active.
        """
        # if self.booster_on:
        self.force[0] += self.booster_speed * cos(self.rotation)
        self.force[1] += self.booster_speed * sin(self.rotation)

    def shoot(self, ent_list, damage, speed):
        proj = Projectile(self, speed, damage, 10, self.image)
        ent_list.append(proj)

    def stabilize_orbit(self, body, counter_clockwise=True):
        # Get the difference between self's target & current velocities.
        targ_vel = self.get_orbital_velocity(body, True)
        delta_v = [ # (x,y) components
                   targ_vel[0] - self.vel[0],
                   targ_vel[1] - self.vel[1],
                  ]
        angle = atan2(delta_v[1], delta_v[0]),
        speed = sqrt(delta_v[0] **2 + delta_v[1]),

    def explode(self, body_list):
        self.is_alive = False
        result = []
        n = 7
        explosion_force = 1.50
        for b in range(0, n):
            angle = random() * 2.0 * math.pi
            vel_x = self.vel[0] + explosion_force * cos(angle)
            vel_y = self.vel[1] + explosion_force * sin(angle)
            result.append(Entity(
                            [self.loc[0], self.loc[1]],
                            [vel_x, vel_y],
                            10.0,
                            0.0,
                            self.image_scrap))
        return result

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

