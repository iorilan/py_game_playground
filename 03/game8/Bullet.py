import sys
import pygame
from  pygame.sprite import Sprite,Group


class Bullet(Sprite):
    def __init__(self, setting, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, setting.bullet_width, setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.color = setting.bullet_color
        self.speed_factor = setting.bullet_speed_factor

    def update(self):
        self.rect.y -= self.speed_factor

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
