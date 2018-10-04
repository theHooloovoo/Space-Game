
import pygame
from pygame.locals import *

class Entity:
    def __init__(self, loc, vel, rotation, radius, img_path):
        loc = loc   # list of two floating points (x, y)
        vel = vel   # list of two floating points (x, y)
        rotation = rotation
        radius = radius

        image = pygame.image.load(img_path)

class Enemy(Entity):
    def __init__(self, speed, health):
        speed = speed
        health = health

class Player(Enemy):
    def __init__(self, weapon):
        weapon = weapon # Is a list of weapons

class Projectile(Entity):
    def __init__(self, speed, damage, duration):
        speed = speed
        damage = damage
        duration = duration
        # Owner # How would this get implemented?

# class Guided(Projectile):

class Star(Entity):
    def __init__(self, mass):
        mass = 100

