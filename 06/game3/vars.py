import pygame, sys
from pygame.locals import *
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
    size=[90,20]
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

class brick_mat:
    size=[20,20]
    color=color.ORANGE
    row=5
    col=0
    matrix=[[]]*row

    @staticmethod
    def init():
        brick_mat.col= game_ctx.WINDOW_WIDTH// (brick_mat.size[0]+5)
        y=0
        x1,y1=brick_mat.size[0]+5,brick_mat.size[1]+5
        for r in range(0, brick_mat.row):
            x=0
            brick_mat.matrix[r] = [(0,0)] * brick_mat.col
            for c in range(0, brick_mat.col):
                brick_mat.matrix[r][c] = (x,y)
                x+=x1
            y+=y1
