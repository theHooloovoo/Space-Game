#!/usr/bin/env python3
""" Main entry point for Space Game.

	This file creates most of the resources used throughout the game.
	It also bundles the resources for use in the game state.  this also
	contains the main loop for the game.

	Attributes:
		window (pygame.Surface): The main surface that serves as the
			background onto which the game graphics are drawn.

		cam (level.Camera): View controller for maintaining porper view
			of the player.

		img_ship0 (pygame.Surface) : Enemy ship graphic

		img_ship1 (pygame.Surface) : Player ship graphic

		img_rock1 (pygame.Surface) : Asteroid graphic

		img_sun (pygame.Surface) : The star graphic

		img_shot (pygame.Surface) : Projectile graphics

		ent_list (entity.Entity[]) : List of entities

		star_list (entity.Star[]) : List of orbitable stars

		player (entity.Agent) : The player's controller

		lvl1 (level.Level) : The first level of the game
"""

import copy
from copy import copy

# Use pygame library
import pygame

from states import MenuState, push, top, size
from entity import Agent, Entity, Star
from level import Camera, Level
import levels

# Used to write on the screen
# font = pygame.font.SysFont("monospace", 12)

# Used for object serialization into JSON format
#import pickle

# pylint: disable=C0103
pygame.init()
pygame.font.init()
window = pygame.display.set_mode([1280, 800])
cam = Camera()
cam.move_to([0.0, 0.0])

img_ship0 = pygame.image.load("resource/cursor.png")
img_ship1 = pygame.image.load("resource/ship1.png")
img_rock1 = pygame.image.load("resource/asteroid_1.png")
img_sun = pygame.image.load("resource/nasa_sun.png")
img_shot1 = pygame.image.load("resource/projectile1.png")

e = Entity([-100, 100], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1)
e2 = copy(e)
a = Agent([-300, 0], [1.00, 1.00], 1.0, 12.0, 0.0, 0.1, 2, img_ship0, img_shot1)
a2 = copy(a)

# player = Player( [400.0, 400.0], [1.00, 1.00], 50.0, 0.0, 0.1, 100, img)
ent_list = []
star_list = []

star_list.append(Star([0.0, 0.0], [0.0, 0.0], 30.0, 400.0, img_sun))
player = Agent([300, 0], [0.0, 0.0], 3.0, 20.0, 0.0, 0.02, 100, img_ship1, img_shot1)
player.vel = player.get_orbital_velocity(star_list[0])

lvl1 = Level(player, ent_list, [], star_list)
# pylint: enable=C0103

#                   Location      Velocity        Mass  Radius Rotation
lvl1.add_ent(Entity([-100, 100], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([100, -100], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([100, 100], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([-100, -100], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([200, -200], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([125, 125], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([125, -125], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([-125, 125], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([-125, -125], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([150, 0], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Entity([-150, 0], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl1.add_ent(Agent([-300, 0], [1.00, 1.00], 1.0, 12.0, 0.0, 0.1, 2, img_ship0, img_shot1))

lvl2 = copy(lvl1)
# lvl1.add_ent(Star( [-700.0, 0.0], [0.0, 0.0], 10.0, 50.0, img_sun))

for e in lvl1.entity_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])
for e in lvl1.agent_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])

push(MenuState(levels.level_list))
while size() > 0:
    top().run(window)
