#!/usr/bin/env python3

from entity import Entity, Agent, Projectile, Star
from level import Level
from gui import Button

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
	def __init__(self, lvl):
		self.background = pygame.image.load("resource/menu_backdrop.jpg")
		self.buttons = [Button(pygame.image.load("resource/play_button.png"),
            [475, 300, 250, 75], lambda : push(GameState(lvl))),
            Button(pygame.image.load("resource/option_button.png"),
            [475, 400, 250, 75], lambda : push(0)),
            Button(pygame.image.load("resource/exit_button.png"),
            [475, 500, 250, 75], lambda : pop())]

	def activate(self):
		self.index = 0
		self.buttons[self.index].highlight(True)

	def deactivate(self):
		pass

	def run(self, window):
		""" Monitors user input for menu selections """
		for event in pygame.event.get():
			if (event.type == pygame.KEYUP):
				if (event.key == pygame.K_ESCAPE):
					pop()
				elif (event.key == pygame.K_w or event.key == pygame.K_UP):
					if (self.index >= 1):
						self.buttons[self.index].highlight(False)
						self.index -= 1
						self.buttons[self.index].highlight(True)
				elif (event.key == pygame.K_s or event.key == pygame.K_DOWN):
					if (self.index < len(self.buttons) - 1):
						self.buttons[self.index].highlight(False)
						self.index += 1
						self.buttons[self.index].highlight(True)
				elif (event.key == pygame.K_RETURN):
					self.buttons[self.index].click()
		window.fill([0,0,0])
		window.blit(self.background, [0,0])
		for btn in self.buttons:
			btn.draw(window)

		pygame.display.flip()

class GameState(State):
	""" The controller for the game """
	def __init__(self, lvl):
		self.frame_count = 0
		self.level = lvl
		self.delta_time = 1.0
		self.timer = pygame.time.Clock()
		self.elapsed_time = self.timer.tick()

	def activate(self):
		pass

	def deactivate(self):
		pass

	def run(self, window):
		self.frame_count += 1
		dt = self.timer.tick()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				pop()
				break
			if event.type is KEYDOWN:
				if event.key == pygame.K_w:
					self.level.player.booster_on = True
					# print("Booster On.")
				if event.key == pygame.K_a:
					self.level.player.is_turning_left = True
				if event.key == pygame.K_d:
					self.level.player.is_turning_right = True
				if event.key == pygame.K_SPACE:
					self.level.projectile_list.append(self.level.player.shoot(5.0, 30.0, 10.0))
					# print(type(self.level.player.shoot(5.0, 30.0, 10.0)))
			if event.type is KEYUP:
				if event.key == pygame.K_w:
					self.level.player.booster_on = False
				if event.key == pygame.K_a:
					self.level.player.is_turning_left = False
				if event.key == pygame.K_d:
					self.level.player.is_turning_right = False
		# Physics
		self.level.step_physics(dt * 0.07)
		# Game Logic
		self.level.step_game_logic(dt)
		# Paint
		self.level.draw_all(window)
		# Quit if player dies
		if self.level.player.is_active == False:
			pop()

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
