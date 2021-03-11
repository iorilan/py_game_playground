"""
move a cat image on screen
"""

import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255,255,255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'
SPEED=5
BORDER = [10,10,700,500]

while True:
    DISPLAYSURF.fill(WHITE)

    if direction == 'right':
        catx += SPEED
        if catx == BORDER[2]:
            direction = 'down'
    elif direction == 'down':
        caty += SPEED
        if caty == BORDER[3]:
            direction = 'left'
    elif direction == 'left':
        catx -= SPEED
        if catx == BORDER[0]:
            direction = 'up'
    elif direction == 'up':
        caty -= SPEED
        if caty == BORDER[1]:
            direction = 'right'

    DISPLAYSURF.blit(catImg,(catx,caty))

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)