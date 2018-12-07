#!/usr/bin/env python3
""" Application States

	This file contains all of the "states" that define how the application
	behaves.  This also provides flow control for the program modeled after
	pushdown automata.  It contains stack data structure methods.

	Attributes:
		states (State[]): The list (behaving as a stack) for all current game
			states.  This has stack methods that are module scoped.
"""

import copy
from copy import copy

import sys
import pygame

from gui import Button, TextButton

class State:
    """ Base class for all game "states" """
    def __init__(self):
        pass

    def activate(self):
        """ Called whenever the state moves to the top of the stack """
        pass

    def deactivate(self):
        """ Called whenever the state is no longer the top of the stack """
        pass

    def run(self, window):
        """ Called iteratively while the state is the top of the stack """
        pass

class PauseState(State):
    """ The controller for the pause menu """
    def __init__(self, bg_entities, cam):
        State.__init__(self)
        self.font = pygame.font.Font("resource/courbd.ttf", 40)
        self.camera = cam
        self.bg_entities = bg_entities
        self.background = pygame.image.load("resource/pause_menu.png")
        self.menu_location = [465, 150]
        self.index = 0
        self.buttons = [Button(pygame.image.load("resource/return_button.png"),
                               [515, 320, 250, 75], lambda: pop()),
                        Button(pygame.image.load("resource/option_button.png"),
                               [515, 430, 250, 75], lambda: push(0)),
                        Button(pygame.image.load("resource/exit_button.png"),
                               [515, 540, 250, 75], lambda: sys.exit())]

    def activate(self):
        self.index = 0
        self.buttons[self.index].highlight(True)

    def deactivate(self):
        pass

    def run(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pop()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.index >= 1:
                        self.buttons[self.index].highlight(False)
                        self.index -= 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.index < len(self.buttons) - 1:
                        self.buttons[self.index].highlight(False)
                        self.index += 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_RETURN:
                    self.buttons[self.index].click()
        window.fill([0, 0, 0])
        for ent in self.bg_entities:
            ent.draw(window, self.camera)
        window.blit(self.background, self.menu_location)

        pos = self.font.size("Paused")
        pos = [self.menu_location[0] + 175 - (pos[0] / 2),
               self.menu_location[1] + 85 - (pos[1] / 2)]
        window.blit(self.font.render("Paused", True, [38, 38, 38]), pos)

        for btn in self.buttons:
            btn.draw(window)
        pygame.display.flip()

class LevelSelectState(State):
    """ The controller for a level selector menu """
    def __init__(self, bg, lvls):
        State.__init__(self)
        self.levels = []
        for i in lvls:
            self.levels.append(copy(i))
        self.font = pygame.font.Font("resource/courbd.ttf", 36)
        self.background = bg
        self.index = 0
        self.buttons = []
        # Make buttons
        count = 0
        cur_width = 0
        cur_height = 0
        for i in lvls:
            count += 1
            s = "Level " + str(count)
            self.buttons.append(
                TextButton(self.font, s,
                [cur_width + 100, cur_height + 150], 0))
            cur_width += 50 + self.font.size(s)[0]
            if cur_width >= 1180:
                cur_height += self.font.size(s)[1] + 50
                cur_width = 0

    def select_level(self):
        """ Selects the level based on the current index of the buttons """
        push(GameState(copy(self.levels[self.index])))

    def activate(self):
        self.index = 0
        self.buttons[self.index].highlight(True)

    def deactivate(self):
        pass

    def run(self, window):
        """ Runs the event loop for the menu
            this entails navigation of the menu
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pop()
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.index >= 1:
                        self.buttons[self.index].highlight(False)
                        self.index -= 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.index < len(self.buttons) - 1:
                        self.buttons[self.index].highlight(False)
                        self.index += 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_RETURN:
                    # self.buttons[self.index].click()
                    self.select_level()
        window.fill([0, 0, 0])
        window.blit(self.background, [0, 0])

        pos = self.font.size("Select Level")
        pos = [window.get_width() / 2 - (pos[0] / 2),
               window.get_height() / 8 - (pos[1] / 2)]
        window.blit(self.font.render("Select Level", True, [250, 250, 250]), pos)

        for btn in self.buttons:
            btn.draw(window)

        pygame.display.flip()

class MenuState(State):
    """ The controller for the main menu """
    def __init__(self, lvls):
        State.__init__(self)
        self.internal_levels = copy(lvls)
        self.font = pygame.font.Font("resource/courbd.ttf", 60)
        self.background = pygame.image.load("resource/menu_backdrop.jpg")
        self.index = 0
        self.buttons = [Button(pygame.image.load("resource/play_button.png"),
                               [515, 300, 250, 75], lambda: push(GameState(lvls[0]))),
                        Button(pygame.image.load("resource/levels_button.png"),
                               [515, 400, 250, 75],
                               lambda: push(LevelSelectState(self.background, self.internal_levels))),
                        Button(pygame.image.load("resource/exit_button.png"),
                               [515, 500, 250, 75], lambda: pop())]

    def activate(self):
        for btn in self.buttons:
            btn.highlight(False)
        self.index = 0
        self.buttons[self.index].highlight(True)

    def deactivate(self):
        self.buttons[0].command = Button(pygame.image.load("resource/play_button.png"),
                               [515, 300, 250, 75], lambda: push(GameState(copy(self.internal_level)))),

    def run(self, window):
        """ Monitors user input for menu selections """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pop()
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.index >= 1:
                        self.buttons[self.index].highlight(False)
                        self.index -= 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.index < len(self.buttons) - 1:
                        self.buttons[self.index].highlight(False)
                        self.index += 1
                        self.buttons[self.index].highlight(True)
                elif event.key == pygame.K_RETURN:
                    self.buttons[self.index].click()
        window.fill([0, 0, 0])
        window.blit(self.background, [0, 0])

        pos = self.font.size("Space Game")
        pos = [window.get_width() / 2 - (pos[0] / 2),
               window.get_height() / 4 - (pos[1] / 2)]
        window.blit(self.font.render("Space Game", True, [150, 150, 150]), pos)

        for btn in self.buttons:
            btn.draw(window)

        pygame.display.flip()

class GameState(State):
    """ The controller for the game """
    def __init__(self, lvl):
        State.__init__(self)
        self.frame_count = 0
        self.level = lvl
        self.delta_time = 1.0
        self.timer = pygame.time.Clock()
        self.elapsed_time = self.timer.tick()

    def activate(self):
        self.timer = pygame.time.Clock()

    def deactivate(self):
        pass

    def run(self, window):
        self.frame_count += 1
        deltatime = self.timer.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                ents = self.level.entity_list + self.level.star_list + self.level.agent_list
                push(PauseState(ents, self.level.cam))
                break
            elif event.type is pygame.KEYDOWN:
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
            elif event.type is pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.level.player.booster_on = False
                if event.key == pygame.K_a:
                    self.level.player.is_turning_left = False
                if event.key == pygame.K_d:
                    self.level.player.is_turning_right = False

        # Physics
        self.level.step_physics(deltatime * 0.07)
        # Game Logic
        self.level.step_game_logic(deltatime)
        # Paint
        self.level.draw_all(window)
        # Quit if player dies
        if not self.level.player.is_active:
            pop()

# pylint: disable=C0103
# Current states of the program
states = []
# pylint enable=C0103

def size():
    """ Returns the size of the stack of states. """
    return len(states)

def top():
    """ Returns the top state in the stack """
    global states
    return states[len(states) - 1]

def push(state):
    """ Pushes a new game state to the state stack.

        Arguments:
        state -- the new state
    """
    global states
    # if any deactivate the current top state
    if states:
        top().deactivate()
    states.append(state)
    # activate the new top state
    top().activate()

def pop():
    """ Pops the top game state and returns it. """
    global states
    # if any deactivate the top state and pop it
    if states:
        top().deactivate()
        state = states.pop()
        # if any activate the new top state
        if states:
            top().activate()
    return state
