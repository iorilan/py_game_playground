import pygame, sys
from pygame.locals import *
def move(game_ctx, black, blue):
    board=game_ctx.board
    rows = len(board)
    cols = len(board[0])
    for r in range(0, rows):
        for c in range(0, cols):
            box = board[r][c]
            if box.color == black:
                box.rect=pygame.draw.rect(game_ctx.DISPLAY_SURF, blue , box.rect)
                box.color=blue
                return

def _move1():
    pass