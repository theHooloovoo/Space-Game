#!/usr/bin/env python3

# Use pygame library
import pygame

from states import MenuState, push, top, size
from entity import Agent, Entity, Star
from level import Camera, Level

cam = Camera()
cam.move_to([0.0, 0.0])

level_list = []

img_enemy1 = pygame.image.load("resource/enemy1.png")
img_ship0 = pygame.image.load("resource/cursor.png")
img_ship1 = pygame.image.load("resource/ship1.png")
img_rock1 = pygame.image.load("resource/asteroid_1.png")
img_sun = pygame.image.load("resource/nasa_sun.png")
img_shot1 = pygame.image.load("resource/projectile1.png")

# Define the first level
star_list1 = []
star_list1.append(Star([0.0, 0.0], [0.0, 0.0], 30.0, 400.0, img_sun))
player1 = Agent([300, 0], [0.0, 0.0], 3.0, 20.0, 0.0, 0.02, 10, img_ship1, img_shot1)
player1.vel = player1.get_orbital_velocity(star_list1[0])
lvl1 = Level(player1, [], [], star_list1)
lvl1.add_ent(Agent([-300, 0], [1.00, 1.00], 1.0, 12.0, 0.0, 0.1, 2, img_ship0, img_shot1))
for e in lvl1.entity_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])
for e in lvl1.agent_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])

# Define the second level
star_list2 = []
star_list2.append(Star([0.0, 0.0], [0.0, 0.0], 30.0, 400.0, img_sun))
player2 = Agent([300, 0], [0.0, 0.0], 3.0, 20.0, 0.0, 0.02, 10, img_ship1, img_shot1)
player2.vel = player2.get_orbital_velocity(star_list2[0])
lvl2 = Level(player2, [], [], star_list2)
lvl2.add_ent(Agent([-300, 0], [1.00, 1.00], 1.0, 12.0, 0.0, 0.1, 2, img_ship0, img_shot1))
lvl2.add_ent(Entity([-150, 0], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([ 150, 0], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([0, -150], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([0,  150], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Agent([-270, 0], [1.00, 1.00], 1.0, 15.0, 0.0, 20, 20, img_enemy1, img_shot1))
lvl2.add_ent(Entity([ 127.6,  127.6], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([-127.6,  127.6], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([ 127.6, -127.6], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
lvl2.add_ent(Entity([-127.6, -127.6], [0.00, 0.00], 10.0, 14.0, 0.0, img_rock1))
for e in lvl2.entity_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])
for e in lvl2.agent_list:
    e.vel = e.get_orbital_velocity(lvl1.star_list[0])

# Define the third level
star_list3 = []
star_list3.append(Star([0.0, 0.0], [0.0, 0.0], 20.0, 50.0, img_sun))
star_list3.append(Star([600.0, 0.0], [0.0, 0.0], 20.0, 50.0, img_sun))
player3 = Agent([-100, 0], [0.0, 0.0], 3.0, 20.0, 0.0, 0.02, 10, img_ship1, img_shot1)
player3.vel = player3.get_orbital_velocity(star_list1[0])
lvl3 = Level(player3, [], [], star_list3)
lvl3.add_ent(Agent([700, 0], [1.00, 1.00], 1.0, 12.0, 0.0, 0.1, 2, img_ship0, img_shot1))
lvl3.player.vel = lvl3.player.get_orbital_velocity(lvl3.star_list[0])
lvl3.agent_list[0].vel = lvl3.agent_list[0].get_orbital_velocity(lvl3.star_list[1])
for e in lvl3.entity_list:
    e.vel = e.get_orbital_velocity(lvl3.star_list[1])
for e in lvl3.agent_list:
    e.vel = e.get_orbital_velocity(lvl3.star_list[1])

level_list = [lvl1, lvl2, lvl3]
