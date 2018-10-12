#!/usr/bin/env python3

from entity import Entity, Enemy, Player, Projectile, Star
from level import Level

import sys
import pygame
from pygame.locals import *

__author__ = "Silas Agnew"

class State:
    """ Base class for all game "states" """
    def __init__(self):
        pass

    def activate(self):
        """ Called whenever the state moves to the top of the stack """
        print("State activate")

    def deactivate(self):
        """ Called whenever the state is no longer the top of the stack """
        print("State deactivate")

    def run(self, window):
        """ Called iteratively while the state is the top of the stack """
        print("State run")

class PauseState(State):
	""" The controller for the pause menu """
	def __init__(self):
		pass
	
	def activate(self):
		pass

	def deactivate(self):
		pass

	def run(self, window):
		pass

class MenuState(State):
	""" The controller for the main menu """
	def __init__(self):
		self.background = pygame.image.load("bgimg.png")
	
	def activate(self):
		print("Menu activate")

	def deactivate(self):
		print("Menu deactivate")
	
	def run(self, window):
		""" """
		for event in pygame.event.get():
			if (event.type == pygame.KEYUP):
				if (event.key == pygame.K_ESCAPE):
					pop()
				elif (event.key == pygame.K_A or event.key == pygame.K_UP):
					pass # Select up
				elif (event.key == pygame.K_S or event.key == pygame.K_DOWN):
					pass # Select down
				elif (event.key == pygame.K_RETURN):
					pass # Load selected state
		print("Menu run ")

class GameState(State):
	""" The controller for the game """
	def __init__(self):
		self.ent_list = []
		self.star_list = []		
		
		self.ent_list.append(Entity([400.0, 400.0], [0.00, 1.00], 10.0, 0.0, "img.png"))
		self.ent_list.append(Entity([500.0, 400.0], [0.00, 3.50], 10.0, 45.0, "img.png"))
		self.ent_list.append(Entity([110.0, 100.0], [0.50, -0.20], 10.0, 45.0, "img.png"))
		self.ent_list.append(Entity([100.0, 110.0], [0.00, 0.50], 10.0, 45.0, "img.png"))
		
		self.star_list.append(Star([600.0, 400.0], [0.0, 0.0], 100.0, 100000.0, "img.png"))
		self.star_list.append(Star([1000.0, 700.0], [0.0, 0.0], 100.0, 1000.0, "img.png"))
		
		self.delta_time = 5.0

	def activate(self):
		pass

	def deactivate(self):
		pass

	def run(self, window):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				pop()
				break

		# Physics
		for e in self.ent_list:
			e.iterate_force(self.star_list)
		
		for e in self.ent_list:
			e.iterate_velocity(self.delta_time)

		for e in self.ent_list:
			e.iterate_location(self.delta_time)

		# Paint
		window.fill([0,0,0])
		for s in self.star_list:
			s.draw(window)
		for e in self.ent_list:
			e.draw(window)

		pygame.display.flip()


# Current states of the program
states = []

def size():
	""" """
	return len(states)

def top():
	""" Returns the top state in the stack """
	global states
	return states[len(states) - 1]

def push(state):
	"""
		Pushes a new game state to the state stack.
		
		Arguments:
		state -- the new state
	"""
	global states
	# if any deactivate the current top state
	if (len(states) > 0):
		top().deactivate()
	states.append(state)
	# activate the new top state
	top().activate()

def pop():
	""" Pops the top game state and returns it. """
	global states
	# if any deactivate the top state and pop it
	if (len(states) > 0):
		top().deactivate()
		state = states.pop()
		# if any activate the new top state
		if (len(states) > 0):
			top().activate()
	return state

