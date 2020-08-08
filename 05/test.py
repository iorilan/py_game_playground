"""
draw part (x,y,width,height) of image on screen (x1,y1)
"""


import pygame, sys, random
from pygame.locals import *

class context:
    img = None
    screen = None
def update_screen(img_rect):
    print(img_rect)
    context.screen.fill((0,255,255))
    context.screen.blit(context.img, (100, 100),img_rect)
    

def main():
    pygame.init()
    pygame.display.set_caption('Puzzle Game')
    context.screen = pygame.display.set_mode((600,480))
    context.img = pygame.image.load('1.png')
    w,h=context.img.get_width(),context.img.get_height()
    
    arr=[]
    for x in range(0,w,10):
        for y in range(0,h,10):
            arr.append([x,y])
    

    running = True
    
    i=0
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        idx = i%(len(arr)-1)
        update_screen((arr[idx][0],arr[idx][1],50,50))
        pygame.time.wait(200)
        pygame.display.flip()
        i+=1
        

if __name__ == '__main__':
    main()