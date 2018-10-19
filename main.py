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
cam = Camera()
cam.move_to([400.0, 400.0])

img = pygame.image.load("img.png")
# image_rect = image.get_rect()

# player = Player( [400.0, 400.0], [1.00, 1.00], 50.0, 0.0, 0.1, 100, img)
player = Agent( [0.0, 0.0], [0.0, 0.0], 50.0, 0.0, 0.1, 100, img)

ent_list = []
star_list = []

ent_list.append(Entity([-100, 100], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([100, -100], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([200,  200], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([-200, 200], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Entity([200, -200], [0.00,  0.00],  50.0,  0.0, img))
ent_list.append(Agent( [-200, -200], [1.00, 1.00], 50.0, 0.0, 0.1, 100, img))

star_list.append(Star( [0.0, 0.0], [0.0, 0.0], 100.0, 100000000000000.0, img))
# star_list.append(Star( [1000.0, 700.0], [0.0, 0.0], 100.0, 1000.0, img))

for e in ent_list:
    v = e.get_orbital_velocity(star_list[0])
    e.vel = v

delta_time = 1.0

lvl1 = Level(player, ent_list, [], star_list)

while 1:

    # Quit when the window gets closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type is KEYDOWN:
            if event.key == pygame.K_SPACE:
                ent_list[5].use_booster()
                print("BOOSTING!")
            if event.key == pygame.K_a:
                cam.zoom_in(0.1)
            if event.key == pygame.K_KP_PLUS:
                cam.zoom_in(-0.1)

    # Physics Loop ====================
    for e in ent_list:
        e.iterate_force(star_list)

    for e in ent_list:
        e.iterate_velocity(delta_time)

    for e in ent_list:
        e.iterate_location(delta_time)
        e.clear_force()
        # e.look_at(star_list[0])
        if type(e) == Agent:
            e.point_to(cam.pointer_game_space(window, pygame.mouse.get_pos()))

    # Paint ===========================
    window.fill([0,0,0])
    for s in star_list:
        s.draw(window, cam)
    for e in ent_list:
        e.draw(window, cam)

    pygame.display.flip()

    pressed_names = []
    if len(pressed_names) != 0:
        print(pressed_names)

push(GameState())
while (size() > 0):
	top().run(window)
  
