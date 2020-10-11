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

class ball:
    speed_x=10
    speed_y=10
    color=color.GREEN
    size=[20,20]
    x=(game_ctx.WINDOW_WIDTH+20)//2
    y=game_ctx.WINDOW_HEIGHT-20


def run():
    pygame.init()
    game_ctx.init()
    pygame.display.set_caption('bouncing ball')
    
def update_screen():
    game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)
    pygame.draw.ellipse(game_ctx.DISPLAY_SURF, ball.color, (ball.x, ball.y, ball.size[0], ball.size[1]))
    x,y=ball.x,ball.y
    if x < 0 or x >= game_ctx.WINDOW_WIDTH-ball.size[0]:
        ball.speed_x=-ball.speed_x
    if y < 0 or y >= game_ctx.WINDOW_HEIGHT-ball.size[1]:
        ball.speed_y=-ball.speed_y
    ball.x+=ball.speed_x
    ball.y+=ball.speed_y

run()
while True:
    update_screen()
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    game_ctx.FPSCLOCK.tick(game_ctx.FPS)