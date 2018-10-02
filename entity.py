
import pygame
from pygame.locals import *

class Entity:
    loc = [0.0, 0.0]
    vel = [0.0, 0.0]
    rotation = 0
    radius = 0

    image = pygame.image.load("img.png")

