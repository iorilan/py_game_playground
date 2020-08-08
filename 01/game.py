"""
-get screen object
    screen = pygame.display.set_mode([500,500])
    fill with color :screen.fill((255,255,255))
-draw circle 
    pygame.draw.circle(screen, (0,0,255),(250,250),75)
-refresh screen
    pygame.display.flip()
-event loop
for e in pygame.event.get()


"""

import pygame

pygame.init()

screen = pygame.display.set_mode([500,500])
color1,color2=(0,0,255),(0,255,0)
running=True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        #...
    
    screen.fill((255,255,255))

    pygame.draw.circle(screen, color1,(250,250),75)

    pygame.display.flip()
    pygame.time.wait(1000)
    color1,color2=color2,color1

pygame.quit()