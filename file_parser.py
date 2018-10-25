#!/usr/bin/env python3

import entity
from entity import *

import pickle

#Files that are serialized
file_in = open("level_1.txt", "wb")

list = []
list.append(Entity([-100,  100], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([100,  -100], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([100,   100], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([-100, -100], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([200,  -200], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([125,   125], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([125,  -125], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([-125,  125], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([-125, -125], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([150,     0], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Entity([-150,    0], [0.00,  0.00],  10.0, 14.0,  0.0))
list.append(Agent( [-300,  0.0], [1.00,  1.00],   1.0, 12.0,  0.0))

class Parser:
	def __init__(self, objects):
		self.objects = objects

	#Pickles the file for loading levels
	def pickleFile(self, objects):
		main_list = []
		for objects in list:
			main_list.append(pickle.dump(objects, file_in))

	file_in.close()

	#Unpickles the file to load the objects for a given level
	def unpickleFile(self, objects):
		objects = []		
		with (open("level_1.txt", "rb")) as openfile:
			while True:
				try:
					objects.append(pickle.load(openfile))
				except EOFError:
					break
