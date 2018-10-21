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
window = pygame.display.set_mode([1280, 800])
cam = Camera()
cam.move_to([0.0, 0.0])

img = pygame.image.load("img.png")
# image_rect = image.get_rect()

# player = Player( [400.0, 400.0], [1.00, 1.00], 50.0, 0.0, 0.1, 100, img)
ent_list = []
star_list = []

star_list.append(Star( [0.0, 0.0], [0.0, 0.0], 100.0, 100000000000000.0, img))
player = Agent( [150.0, 0.0], [0.0, 0.0], 50.0, 0.0, 0.1, 100, img)
player.vel = player.get_orbital_velocity(star_list[0])

lvl1 = Level(player, ent_list, [], star_list)

lvl1.add_ent(Entity([-100, 100], [0.00,  0.00],  50.0,  0.0, img))
lvl1.add_ent(Entity([100, -100], [0.00,  0.00],  50.0,  0.0, img))
lvl1.add_ent(Entity([200,  200], [0.00,  0.00],  50.0,  0.0, img))
lvl1.add_ent(Entity([-200, 200], [0.00,  0.00],  50.0,  0.0, img))
lvl1.add_ent(Entity([200, -200], [0.00,  0.00],  50.0,  0.0, img))
lvl1.add_ent(Agent( [-200, -200], [1.00, 1.00], 50.0, 0.0, 0.1, 100, img))

# star_list.append(Star( [1000.0, 700.0], [0.0, 0.0], 100.0, 1000.0, img))

print("Entities:\t", len(lvl1.entity_list))
print("Stars:\t", len(lvl1.star_list))
print("Agents:\t", len(lvl1.agent_list))
print("Projectiles:\t", len(lvl1.projectile_list))

for e in ent_list:
    v = e.get_orbital_velocity(star_list[0])
    e.vel = v

delta_time = 1.0

initial_point = [10, 5]
print(lvl1.cam.loc)
gs_ss = lvl1.cam.get_screen_space(window, initial_point)
ss_gs = lvl1.cam.pointer_game_space(window, gs_ss)
end_point = lvl1.cam.get_screen_space(window, ss_gs)
print(initial_point, "->", gs_ss, "->", ss_gs, "->", end_point)

"""
while 1:

    # Check Events ====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type is KEYDOWN:
            if event.key == pygame.K_SPACE:
                lvl1.player.use_booster()
                print("BOOSTING!")
            if event.key == pygame.K_MINUS:
                cam.zoom_in(0.05)
            if event.key == pygame.K_EQUALS:
                cam.zoom_in(-0.05)

    lvl1.cam.move_to(lvl1.player.get_location())
    # Physics Loop ====================
    lvl1.step_physics(delta_time)
    lvl1.player.point_to(cam.pointer_game_space(window, pygame.mouse.get_pos()))
    # Paint ===========================
    lvl1.draw_all(window)

    pressed_names = []
    if len(pressed_names) != 0:
        print(pressed_names)
"""

push(GameState(lvl1))
while (size() > 0):
	top().run(window)
  
