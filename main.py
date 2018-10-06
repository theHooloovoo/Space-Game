#!/usr/bin/env python3

from entity import Entity, Enemy, Player, Projectile, Star
from level import Level

import sys
# Use the pygame library
import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode([1200, 800])

# image = pygame.image.load("img.png")
# image_rect = image.get_rect()

ent_list = []
star_list = []

ent_list.append(Entity([400.0, 400.0], [0.00, 1.00], 10.0, 0.0, "img.png" ))
ent_list.append(Entity([500.0, 400.0], [0.00, 3.50], 10.0, 45.0, "img.png" ))
ent_list.append(Entity([110.0, 100.0], [0.50, -0.20], 10.0, 45.0, "img.png" ))
ent_list.append(Entity([100.0, 110.0], [0.00, 0.50], 10.0, 45.0, "img.png" ))

star_list.append(Star( [600.0, 400.0], [0.0, 0.0], 100.0, 100000.0, "img.png" ))
star_list.append(Star( [1000.0, 700.0], [0.0, 0.0], 100.0, 1000.0, "img.png" ))

delta_time = 5.0

while 1:

    # Quit when the window gets closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Physics Loop ====================
    for e in ent_list:
        e.iterate_force(star_list)

    for e in ent_list:
        e.iterate_velocity(delta_time)

    for e in ent_list:
        e.iterate_location(delta_time)

    # Paint ===========================
    window.fill([0,0,0])
    for s in star_list:
        s.draw(window)
    for e in ent_list:
        e.draw(window)

    pygame.display.flip()

