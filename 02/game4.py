import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800,600))
pygame.display.set_caption('hello world')

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,128)

fontObj = pygame.font.Font('FreeSansBold.ttf', 32)
textSurfaceObj = fontObj.render('Hello World!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200,150)


FPS = 10
fpsClock = pygame.time.Clock()
BORDER= [10,10,700,500]
SPEED=3
dir = 'r'
while True:    
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    if dir == 'r' :
        textRectObj[0]+=SPEED
        if textRectObj[0] > BORDER[2]:
            dir = 'd'
    elif dir == 'd':
        textRectObj[1] += SPEED
        if textRectObj[1] > BORDER[3]:
            dir = 'l'
    elif dir == 'l':
        textRectObj[0] -= SPEED
        if textRectObj[0] < BORDER[0]:
            dir = 'u'
    elif dir == 'u':
        textRectObj[1] -= SPEED
        if textRectObj[1] < BORDER[1]:
            dir = 'r'

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)

