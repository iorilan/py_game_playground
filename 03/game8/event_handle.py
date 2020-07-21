import sys,time
import pygame
from  pygame.sprite import Sprite,Group

from Settings import Settings
from GameStats import GameStats
from Button import Button
from Ship import Ship 
from Alien import Alien 
from Bullet import Bullet

class event_context():
    def __init__(self, setting, screen, stats, scoreboard):
        self.setting = setting
        self.screen = screen
        self.stats = stats
        self.scoreboard = scoreboard


def check_events(ctx):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            check_keydown(e, ctx)
        elif e.type == pygame.KEYUP:
            check_keyup(e,ctx)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            play_button_clicked= ctx.play_button.rect.collidepoint(x, y)
            if play_button_clicked and not ctx.stats.game_active:
                game_start(ctx)

def check_keydown(e, ctx):
    if e.key == pygame.K_RIGHT :
        ctx.ship.moving_right = True
    elif e.key == pygame.K_LEFT:
        ctx.ship.moving_left = True
    elif e.key == pygame.K_SPACE:
        if len(ctx.bullets) < ctx.setting.bullets_allowed:
            ctx.bullets.add(Bullet(ctx.setting, ctx.screen, ctx.ship))
    elif e.key == pygame.K_q:
        sys.exit()

def check_keyup(e, ctx):
    if e.key == pygame.K_RIGHT :
        ctx.ship.moving_right = False
    elif e.key == pygame.K_LEFT:
        ctx.ship.moving_left = False

def game_start(ctx):
    ctx.setting.reset()
    pygame.mouse.set_visible(False)
    ctx.stats.reset()
    ctx.stats.game_active = True

    ctx.aliens.empty()
    ctx.bullets.empty()

    create_aliens(ctx)
    ctx.ship.to_center()

    ctx.scoreboard.update_score()
    ctx.scoreboard.try_update_highest()
    ctx.scoreboard.update_game_level()
    ctx.scoreboard.update_left_ships()

def create_aliens(ctx):
    alien = Alien(ctx.setting, ctx.screen , 0)
    alien_width,alien_height = alien.rect.width, alien.rect.height

    space_x = ctx.setting.screen_width-2 * alien_width
    space_y = ctx.setting.screen_height-(3 * alien_height)-ctx.ship.rect.height

    rows = int(space_y/(2 * alien_height))
    cols = int(space_x/(2 * alien_width))

    for r in range(rows):
        for c in range(cols):
            x=alien_width + 2*alien_width*c
            y=alien_height + 2*alien_height*r
            ctx.aliens.add(Alien(ctx.setting, ctx.screen, x, y))

def next_level(ctx):
    ctx.bullets.empty()

    create_aliens(ctx)
    
    ctx.stats.game_level += 1
    ctx.scoreboard.update_game_level()

    ctx.setting.speed_up()

def game_over(ctx):
    if ctx.stats.ships_left > 0:
        ctx.stats.ships_left -= 1
        ctx.scoreboard.update_left_ships()
        print(f'ship left : {ctx.stats.ships_left}')
        ctx.bullets.empty()
        ctx.aliens.empty()

        create_aliens(ctx)
        ctx.ship.to_center()

        time.sleep(0.5)
    else:
        ctx.stats.game_active = False
        pygame.mouse.set_visible(True)

def check_game_over(ctx):
    if pygame.sprite.spritecollideany(ctx.ship, ctx.aliens):
        game_over(ctx)

    screen_rect = ctx.screen.get_rect()
    for a in ctx.aliens.sprites():
        if a.rect.bottom >= screen_rect.bottom:
            game_over(ctx)
            break
