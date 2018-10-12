#!/usr/bin/env python3

from states import *
from entity import *
from level import *

import sys

# Use the pygame library
import pygame
from pygame.locals import *

# Used for object serialization into JSON format
import pickle

pygame.init()
window = pygame.display.set_mode([1200, 800])

img = pygame.image.load("img.png")
# image_rect = image.get_rect()

ent_list = []
star_list = []

ent_list.append(Entity([400.0, 400.0], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([450.0, 400.0], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([500.0, 400.0], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([550.0, 400.0], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([600.0, 200.0], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Enemy( [400.0, 400.0], [1.00, 1.00], 50.0, 0.0, 0.0, 100, img))

star_list.append(Star( [600.0, 400.0], [0.0, 0.0], 100.0, 100000000000000.0, img))
# star_list.append(Star( [1000.0, 700.0], [0.0, 0.0], 100.0, 1000.0, img))

for e in ent_list:
    if type(e) != Enemy:
        v = e.get_orbital_velocity(star_list[0])
        e.vel = v
        print("Orbital Vel:", v[0], v[1])

delta_time = 1.0

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
        e.clear_force()
        e.look_at(star_list[0])

    # Paint ===========================
    window.fill([0,0,0])
    for s in star_list:
        s.draw(window)
    for e in ent_list:
        e.draw(window)

    pygame.display.flip()

push(GameState())
while (size() > 0):
	top().run(window)
  