import pygame, sys, random
from pygame.locals import *
from game_context import ctx
import helper 

def handle_event_keyboard(event):
    if event.key in (K_LEFT, K_a) :
        ctx.SLIDE_TO = ctx.LEFT
    elif event.key in (K_RIGHT, K_d) :
        ctx.SLIDE_TO = ctx.RIGHT
    elif event.key in (K_UP, K_w) :
        ctx.SLIDE_TO = ctx.UP
    elif event.key in (K_DOWN, K_s) :
        ctx.SLIDE_TO = ctx.DOWN
    elif event.key == K_ESCAPE:
        helper.terminate() # terminate if the KEYUP event was for the Esc key

    if ctx.SLIDE_TO and helper.isValidMove(ctx.MAIN_BOARD, ctx.SLIDE_TO):
        helper.makeMove(ctx.MAIN_BOARD, ctx.SLIDE_TO)
        ctx.ALL_MOVES.append(ctx.SLIDE_TO) # record the slide

def handle_event_mouse(event):
    spotx, spoty = helper.getSpotClicked(ctx.MAIN_BOARD, event.pos[0], event.pos[1])
    if (spotx, spoty) == (None, None):
        if ctx.RESET_RECT.collidepoint(event.pos):
            helper.resetAnimation(ctx.MAIN_BOARD, ctx.ALL_MOVES) 
            ctx.ALL_MOVES = []
        elif ctx.NEW_RECT.collidepoint(event.pos):
            helper.renew_game(ctx.TOTAL_NUMBER) 
            ctx.ALL_MOVES = []
        elif ctx.SOLVE_RECT.collidepoint(event.pos):
            helper.resetAnimation(ctx.MAIN_BOARD,ctx.SOLUTION_SEQ+ctx.ALL_MOVES) 
            ctx.ALL_MOVES = []

def handle_event():
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            handle_event_mouse(event)
        elif event.type == KEYUP:
            handle_event_keyboard(event)

def main():
    pygame.init()
    pygame.display.set_caption('Slide Puzzle')

    helper.initialize()

    while True:
        helper.update_screen()
        handle_event()

if __name__ == '__main__':
    main()