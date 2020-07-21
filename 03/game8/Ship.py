import sys
import pygame
from  pygame.sprite import Sprite,Group


class Ship(Sprite):
    def __init__(self, setting, screen):
        super(Ship, self).__init__()
        
        self.screen = screen

        self.image = pygame.image.load("plane.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

        self.setting = setting
        #print(f'{self.rect.x},{self.rect.y},{self.rect.left},{self.rect.top}')

    def blit_me(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.setting.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.rect.x -= self.setting.ship_speed_factor
        
        self.screen.blit(self.image, self.rect)

    def to_center(self):
        self.rect.centerx = self.screen_rect.centerx