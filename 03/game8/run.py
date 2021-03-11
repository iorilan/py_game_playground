"""
    complete space ship game
    score + life count 

    settings
    load sprites(group)
    event context
    main loop:
        handle_events
            keyboard,mouse
        refresh screen
            draw sprite
            collide

"""

import sys
import pygame
from  pygame.sprite import Sprite,Group


from Settings import Settings
from GameStats import GameStats, Scoreboard
from Button import Button
from Ship import Ship 
from Alien import Alien 
from Bullet import Bullet
import event_handle as handler

def update_screen(ctx):
    ctx.screen.fill(ctx.setting.bg_color)

    if not ctx.stats.game_active:
        ctx.play_button.draw()
        pygame.display.flip()
        return
    
    ctx.ship.blit_me()
    #screen.blit(self.image, self.rect)

    #bullets
    for b in ctx.bullets.sprites():
        b.draw_bullet()
    #ctx.bullets.draw() only apply for image
    
    ctx.bullets.update()
    for b in ctx.bullets.copy():
        if b.rect.bottom <= 0:
            ctx.bullets.remove(b)
    
    #aliens
    for a in ctx.aliens.sprites():
        if a.check_edge(): 
            ctx.setting.fleet_direction *= -1
            for a1 in ctx.aliens.sprites():
                a1.rect.y += ctx.setting.fleet_drop_speed
            break
    ctx.aliens.draw(ctx.screen)
    ctx.aliens.update()

    #score
    ctx.scoreboard.blit_me()
    collisions = pygame.sprite.groupcollide(ctx.bullets, ctx.aliens, True, True)
    if collisions:
        for c in collisions.values():
            ctx.stats.score += ctx.setting.alien_points * len(c)
            ctx.scoreboard.update_score()
            ctx.scoreboard.try_update_highest()

    if len(ctx.aliens) == 0:
        handler.next_level(ctx)

    handler.check_game_over(ctx)

    pygame.display.flip()


def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)
    
    ship = Ship(setting, screen)
    bullets = Group()
    aliens = Group()
    
    stats = GameStats(setting)
    scoreboard = Scoreboard(setting, screen, stats)
    play_button = Button(setting, screen, "Play")

    _ctx = handler.event_context(setting, screen, stats, scoreboard)
    _ctx.ship,_ctx.bullets,_ctx.aliens = ship,bullets,aliens
    _ctx.play_button = play_button

    handler.create_aliens(_ctx)
    while True:
        handler.check_events(_ctx)
        update_screen(_ctx)

run_game()
