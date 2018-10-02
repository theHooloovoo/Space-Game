#!/usr/bin/env python3

from entity import Entity, Enemy, Player, Projectile, Star

import sys
# Use the pygame library
import pygame
from pygame.locals import *

loc = [0.0, 0.0]
vel = [1.0, 1.0]

pygame.init()
window = pygame.display.set_mode([1200, 800])

image = pygame.image.load("img.png")
image_rect = image.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    image_rect = image_rect.move(vel)

    window.fill([0,0,0])
    window.blit(image, image_rect)
    pygame.display.flip()

