import sys
import pygame
from  pygame.sprite import Sprite,Group


class Alien(Sprite):
    def __init__(self, setting, screen, x, y=None):
        super(Alien, self).__init__()
        self.screen = screen
        self.setting = setting

        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        if y:
            self.rect.y = y
        else:
            self.rect.y = self.rect.height

    def update(self):
        self.rect.x += self.setting.alien_speed_factor*self.setting.fleet_direction
    
    def check_edge(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
        
