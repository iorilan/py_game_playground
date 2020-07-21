'''
    blit image in screen
    keyboard event handling to move image left right
'''

import sys
import pygame

class Settings():
    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.game_name = "Game"

        self.ship_speed_factor = 1.5
class Ship():
    def __init__(self, setting, screen):
        self.screen = screen

        self.image = pygame.image.load("plane.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

        self.setting = setting

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.setting.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.setting.ship_speed_factor

        self.rect.centerx = self.center

def check_keydown(e, ship):
        if e.key == pygame.K_RIGHT :
            ship.moving_right = True
        elif e.key == pygame.K_LEFT:
            ship.moving_left = True

def check_keyup(e, ship):
        if e.key == pygame.K_RIGHT :
            ship.moving_right = False
        elif e.key == pygame.K_LEFT:
            ship.moving_left = False

def check_events(ship):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            check_keydown(e, ship)
        elif e.type == pygame.KEYUP:
            check_keyup(e,ship)
def update_screen(setting,screen,ship):
    #print(setting.bg_color)
    screen.fill(setting.bg_color)
    ship.blitme()

    pygame.display.flip()


def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)
    ship = Ship(setting, screen)

    # bg_color = (230, 230, 230)
    while True:

        check_events(ship)
        ship.update()
        update_screen(setting, screen, ship)

run_game()
