"""
draw bar+bouncing ball
"""


import pygame, sys
from pygame.locals import *


#DISPLAYSURF.convert_alpha()
class color:
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 128, 0)
    WHITE = (255, 255, 255)

class game_ctx:
    game_over = False
    FPSCLOCK = None
    DISPLAY_SURF = None
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BGCOLOR=color.WHITE
    FPS=30

    @staticmethod
    def init():
        game_ctx.FPSCLOCK = pygame.time.Clock()
        game_ctx.DISPLAY_SURF = pygame.display.set_mode((game_ctx.WINDOW_WIDTH, game_ctx.WINDOW_HEIGHT))

class bar:
    size=[70,20]
    color=color.ORANGE
    x=(game_ctx.WINDOW_WIDTH-70)//2
    y=game_ctx.WINDOW_HEIGHT-20
    speed=10
    moving_left=False
    moving_right=False

    def move(d):
        new_x=bar.x+d
        if new_x <0:
            bar.x=0
        elif new_x>game_ctx.WINDOW_WIDTH-70:
            bar.x=game_ctx.WINDOW_WIDTH-70
        else:
            bar.x+=d

class ball:
    speed_x=10
    speed_y=10
    color=color.BLUE
    size=[20,20]
    x=(game_ctx.WINDOW_WIDTH+20)//2
    y=bar.y-20
    
#https://www.pygame.org/docs/ref/key.html
def handle_event():
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        elif e.type==KEYDOWN:
            if e.key == K_LEFT:
                bar.moving_left = True
            elif e.key == K_RIGHT:
                bar.moving_right = True
        elif e.type==KEYUP:
            if e.key==K_LEFT:
                bar.moving_left=False
            elif e.key == K_RIGHT:
                bar.moving_right=False
        # elif e.type == MOUSEMOTION:
        #     pass
        # elif e.type == MOUSEBUTTONUP:
        #     pass

def run():
    pygame.init()
    game_ctx.init()
    pygame.display.set_caption('bouncing ball')

def check_gameover():
    if ball.y>game_ctx.WINDOW_HEIGHT-ball.size[1]//2:
        game_ctx.game_over=True
def update_screen():
    #screen
    game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)

    #bar
    if bar.moving_left:
        bar.move(-bar.speed)
    elif bar.moving_right:
        bar.move(bar.speed)
    bar_rect=pygame.draw.rect(game_ctx.DISPLAY_SURF, bar.color,(bar.x, bar.y, bar.size[0], bar.size[1]))

    #moving ball
    ball_rect=pygame.draw.ellipse(game_ctx.DISPLAY_SURF, ball.color, (ball.x, ball.y, ball.size[0], ball.size[1]))
    x,y=ball.x,ball.y
    if x < 0 or x >= game_ctx.WINDOW_WIDTH-ball.size[0]:
        ball.speed_x=-ball.speed_x
    if y < 0 or ball_rect.colliderect(bar_rect):
        ball.speed_y=-ball.speed_y
    ball.x+=ball.speed_x
    ball.y+=ball.speed_y
    check_gameover()
    

run()
while not game_ctx.game_over:
    update_screen()

    handle_event()

    pygame.display.update()
    game_ctx.FPSCLOCK.tick(game_ctx.FPS)