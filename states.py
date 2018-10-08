
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

    def run(self):
        """ Called iteratively while the state is the top of the stack """
        print("State run")

class MenuState(State):
    def __init__(self, bgimg):
        #self.background = pygame.image.load(bgimg)

    def activate(self):
        print("Menu activate")

    def deactivate(self):
        print("Menu deactivate")

    def run(self, i):
        i += 1
        if (i > 9):
            State.pop()
        print("Menu run " + str(i))


# Current states of the program
states = []

def push(state):
    """
    :    Pushes a new game state to the state stack.
        
        Arguments:
        state -- the new state
    """
    # if any deactivate the current top state
    if (len(State.states) > 0):
        State.top().deactivate()
    State.states.append(state)
    # activate the new top state
    State.top().activate()

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

def top():
    """ Returns the top state in the stack """
    return State.states[len(State.states) - 1]
