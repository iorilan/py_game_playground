"""
5 chess game
"""

import pygame, sys
from pygame.locals import *
import random
import cpu

class color:
    BLACK = (0,0,0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 128, 0)
    WHITE = (255, 255, 255)

class box:
    def __init__(self, r, c):
        self.rect=r
        self.color=c

class game_ctx:
    game_over = False
    FPSCLOCK = None
    DISPLAY_SURF = None
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BGCOLOR=color.WHITE
    FPS=30
    board= []
    size=50
    margin=5
    rows=0
    cols=0
    unit_color=color.BLACK
    @staticmethod
    def init():
        game_ctx.FPSCLOCK = pygame.time.Clock()
        game_ctx.DISPLAY_SURF = pygame.display.set_mode((game_ctx.WINDOW_WIDTH, game_ctx.WINDOW_HEIGHT))
        game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)

        game_ctx.rows = game_ctx.WINDOW_HEIGHT//(game_ctx.size+game_ctx.margin)
        game_ctx.cols=  game_ctx.WINDOW_WIDTH//(game_ctx.size+game_ctx.margin)
        game_ctx.board = [[]]*game_ctx.rows
        y=0
        for r in range(0, game_ctx.rows):
            x=0
            game_ctx.board[r]=[0]*game_ctx.cols
            for c in range(0, game_ctx.cols):
                rect=pygame.draw.rect(game_ctx.DISPLAY_SURF,game_ctx.unit_color, (x,y,game_ctx.size, game_ctx.size))
                game_ctx.board[r][c]=box(rect, game_ctx.unit_color)
                x+=game_ctx.size+game_ctx.margin
            y+=game_ctx.size+game_ctx.margin

    @staticmethod
    def box_color(player='h'):
        return color.ORANGE if player == 'h' else color.BLUE

def handle_event():
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        elif e.type==MOUSEBUTTONUP:
            handle_click(e)

def clicked_box(x,y):
    for r in range(0, game_ctx.rows):
        for c in range(0, game_ctx.cols):
            box=game_ctx.board[r][c]
            if box.rect.collidepoint(x,y):
                return game_ctx.board[r][c]
    return None

def handle_click(e):
    x,y = e.pos
    box = clicked_box(x,y)
    if not box:
        return
    c = game_ctx.box_color()
    box.rect=pygame.draw.rect(game_ctx.DISPLAY_SURF,c , box.rect)
    box.color=c
    cpu.move(game_ctx, color.BLACK, color.BLUE)

def run():
    pygame.init()
    game_ctx.init()
    pygame.display.set_caption('chess game')

def check_gameover():
    pass

def update_screen():
    pass
    #screen
    #game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)


run()
while not game_ctx.game_over:
    update_screen()

    handle_event()

    pygame.display.update()
    game_ctx.FPSCLOCK.tick(game_ctx.FPS)