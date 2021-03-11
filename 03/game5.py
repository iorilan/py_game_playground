'''
    draw ship + move + shoot 

    (Sprite) Group :
        sprites - get all sprite element to loop through
        add - 
        update - call update on each sprite object
        remove(obj) - delete sprite obj
        empty - remove all
        draw - only can use for sprite has image attribute
            = for s in sprites(): self.screen.blit(self.image, self.rect)

        not image :pygame.draw.rect(screen, color, rect): draw sprite on screen
        
'''

import sys
import pygame
from  pygame.sprite import Sprite,Group

class Settings():
    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.game_name = "Game"

        self.ship_speed_factor = 1.5

        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3


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


def check_keydown(e, ship, setting, screen, bullets):
        if e.key == pygame.K_RIGHT :
            ship.moving_right = True
        elif e.key == pygame.K_LEFT:
            ship.moving_left = True
        elif e.key == pygame.K_SPACE:
            if len(bullets) < setting.bullets_allowed:
                bullets.add(Bullet(setting, screen, ship))

def check_keyup(e, ship):
        if e.key == pygame.K_RIGHT :
            ship.moving_right = False
        elif e.key == pygame.K_LEFT:
            ship.moving_left = False

def check_events(ship, setting, screen, bullets):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            check_keydown(e, ship, setting, screen, bullets)
        elif e.type == pygame.KEYUP:
            check_keyup(e,ship)

def update_screen(setting,screen,ship, bullets):
    #print(setting.bg_color)
    screen.fill(setting.bg_color)
    ship.blitme()

    for b in bullets.sprites():
        b.draw_bullet()

    bullets.update()
    for b in bullets.copy():
        if b.rect.bottom <= 0:
            bullets.remove(b)
        
    pygame.display.flip()


def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)
    ship = Ship(setting, screen)
    bullets = Group()

    # bg_color = (230, 230, 230)
    while True:

        check_events(ship, setting, screen, bullets)
        ship.update()
        update_screen(setting, screen, ship, bullets)

run_game()
