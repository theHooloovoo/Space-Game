
import pygame
from pygame.locals import *

__author__ = "Silas Agnew"

class State:
    """ Base class for all game "states" """

    # Current states of the program
    states = []

    @staticmethod
    def push(state):
        """
            Pushes a new game state to the state stack.

            Arguments:
            state -- the new state
        """
        # if any deactivate the current top state
        if (len(State.states) > 0):
            State.top().deactivate()
        State.states.append(state)
        # activate the new top state
        State.top().activate()

    @staticmethod
    def pop():
        """ Pops the top game state and returns it. """
        # if any deactivate the top state and pop it
        if (len(State.states) > 0):
            State.top().deactivate()
            state = State.states.pop()
            # if any activate the new top state
            if (len(State.states) > 0):
                State.top().activate()
            return state

    @staticmethod
    def top():
        """ Returns the top state in the stack """
        return State.states[len(State.states) - 1]

    def __init__(self):
        pass

    def activate(self):
        """ Called whenever the state moves to the top of the stack """
        print("State activate")
        pass

    def deactivate(self):
        """ Called whenever the state is no longer the top of the stack """
        print("State deactivate")
        pass

    def run(self):
        """ Called iteratively while the state is the top of the stack """
        print("State run")
        pass

class MenuState(State):
    def __init__(self, bgimg):
        #self.background = pygame.image.load(bgimg)
        pass

    def activate(self):
        print("Menu activate")
        pass

    def deactivate(self):
        print("Menu deactivate")
        pass

    def run(self):
        print("Menu run")
        pass

#Tests
State.push(MenuState(0))
State.top().run()
State.pop()
