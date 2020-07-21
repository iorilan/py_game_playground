'''
    for pygame.image.load
    call screen.blit(image, rect) to 'refresh' display in screen
'''

import sys
import pygame

class Settings():
    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.game_name = "Game"

class Ship():
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load("plane.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)

def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)
    ship = Ship(screen)

    #bg_color = (230, 230, 230)
    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(setting.bg_color)
        ship.blitme()
        pygame.display.flip()

run_game()
