"""
update screen test


-create screen with color
screen = pygame.display.set_mode([w,h])
screen.fill((0,255,255))

-event loop
for e in pygame.event.get()

-pressed keys array
pygame.key.get_pressed()


-create surface rect 
surf = pygame.Surface((75,75))
surf.fill((255,255,255))
screen.blit(surf, surf.get_rect())

-refresh screen
pygame.display.flip()

"""

import pygame

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,75))
        self.surf.fill((255,255,255))

        self.center = ((WIDTH-self.surf.get_width())/2,(HEIGHT-self.surf.get_height())/2)
        self.rect = self.surf.get_rect()
        self.rect.left = self.center[0]
        self.rect.top = self.center[1]

        self.step = 1

    def update(self, k):
        #print(k)
        if k[K_UP] and self.rect.top>0:
            self.rect.move_ip(0,-self.step)
        if k[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0,self.step)
        if k[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.step,0)
        if k[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.step,0)

WIDTH = 800
HEIGHT = 600
_screen = pygame.display.set_mode([WIDTH,HEIGHT])
_player = Player()
_running=True

pygame.init()

while _running:

    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                _running = False
        elif e.type == QUIT:
            _running=False
        #...more events
    
    pressed_keys = pygame.key.get_pressed()
    _player.update(pressed_keys)

    _screen.fill((0,255,255))

    #surf = pygame.Surface((50,50))
    #surf.fill((0,0,0))
    # rect = surf.get_rect()
    # surf_center = (
    #     (WIDTH-surf.get_width())/2,
    #     (HEIGHT-surf.get_height())/2
    # )
    #_screen.blit(surf, (WIDTH/2, HEIGHT/2))
    #_screen.blit(surf, surf_center)
    
    _screen.blit(_player.surf, _player.rect)

    pygame.display.flip()

pygame.quit()





