#!/usr/bin/env python3

from states import *
# Use the pygame library
import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode([1200, 800])

# image = pygame.image.load("img.png")
# image_rect = image.get_rect()

push(GameState())
while (size() > 0):
	top().run(window)
