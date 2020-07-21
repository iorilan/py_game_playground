'''
    group to group collide:
        collisions = pygame.sprite.groupcollide(group_1, group_2, True, True)
    obj to group collide:
        pygame.sprite.spritecollideany(obj, group)
    if point[x,y] is in rect:
        pygame.rect.collidepoint(x, y)
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
        self.bullets_allowed = 30

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
    


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
        self.y = float(self.rect.y)

        self.color = setting.bullet_color
        self.speed_factor = setting.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


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

    # def draw(self):
    #     self.screen.blit(self.image, self.rect)
    def update(self):
        self.rect.x += self.setting.alien_speed_factor*self.setting.fleet_direction
    
    def check_edge(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
        

def check_keydown(e, ship, setting, screen, bullets):
        if e.key == pygame.K_RIGHT :
            ship.moving_right = True
        elif e.key == pygame.K_LEFT:
            ship.moving_left = True
        elif e.key == pygame.K_SPACE:
            if len(bullets) < setting.bullets_allowed:
                bullets.add(Bullet(setting, screen, ship))
        elif e.key == pygame.K_q:
            sys.exit()

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

def create_aliens(setting, screen, ship, aliens):
    alien = Alien(setting, screen,0)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    space_x = setting.screen_width-2*alien_width
    space_y = setting.screen_height-(3*alien_height)-ship.rect.height
    rows = int(space_y/(2*alien_height))
    alien_id = int(space_x/(2*alien_width))
    for r in range(rows):
        for alien_number in range(alien_id):
            x=alien_width+2*alien_width*alien_number
            y=alien_height+2*alien_height*r
            aliens.add(Alien(setting, screen, x,y))
    
def update_screen(setting,screen,ship, bullets, aliens):
    #print(setting.bg_color)
    screen.fill(setting.bg_color)
    ship.blitme()

    for b in bullets.sprites():
        b.draw_bullet()
    bullets.update()
    for b in bullets.copy():
        if b.rect.bottom <= 0:
            bullets.remove(b)
    
    for a in aliens.sprites():
        if a.check_edge(): 
            setting.fleet_direction *= -1
            a.rect.y += setting.fleet_drop_speed
            break
    aliens.draw(screen)
    aliens.update()

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_aliens(setting, screen, ship, aliens)

    if pygame.sprite.spritecollideany(ship, aliens):
        print("Game Over")
        
    pygame.display.flip()


def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)
    
    ship = Ship(setting, screen)

    bullets = Group()

    aliens = Group()
    create_aliens(setting, screen, ship, aliens)
    

    # bg_color = (230, 230, 230)
    while True:

        check_events(ship, setting, screen, bullets)
        ship.update()
        update_screen(setting, screen, ship, bullets, aliens)

run_game()
