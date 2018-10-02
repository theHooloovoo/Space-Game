
import pygame
from pygame.locals import *

class Entity:
    loc = [0.0, 0.0]
    vel = [0.0, 0.0]
    rotation = 0
    radius = 0

    image = pygame.image.load("img.png")

class Enemy(Entity):
    speed = 0
    health = 1

class Player(Enemy):
    weapon = []

class Projectile(Entity):
    speed = 1
    damage = 1
    duration = 10
    # Owner # How would this get implemented?

# class Guided(Projectile):

class Star(Entity):
    mass = 100

