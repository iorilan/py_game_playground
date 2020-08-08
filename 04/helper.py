import pygame, sys, random
from pygame.locals import *
from game_context import ctx
import numpy as np


def initialize():
    ctx.FPSCLOCK = pygame.time.Clock()
    ctx.DISPLAYSURF = pygame.display.set_mode((ctx.WINDOWWIDTH, ctx.WINDOWHEIGHT))
    ctx.BASICFONT = pygame.font.Font('freesansbold.ttf', ctx.BASICFONTSIZE)

    offset_x=180
    offset_y=210
    # Store the option buttons and their rectangles in OPTIONS.
    ctx.RESET_SURF, ctx.RESET_RECT = makeText('Reset',    ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y)
    ctx.NEW_SURF,   ctx.NEW_RECT   = makeText('New Game', ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y-70)
    ctx.SOLVE_SURF, ctx.SOLVE_RECT = makeText('Solve',    ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y-140)
    ctx.STEP_SURF, ctx.STEP_RECT = makeText(str(ctx.STEP_TOTAL),    ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y-210)

    renew_game(ctx.TOTAL_NUMBER)
    ctx.SOLVEDBOARD = getStartingBoard() 


def renew_game(steps):
    ctx.SOLUTION_SEQ = []
    ctx.MAIN_BOARD = getStartingBoard()
    lastMove = None
    ctx.TEXT_DISPLAY = 'Generating game...' 
    ctx.STEP_TOTAL=0
    for i in range(steps):
        move = getRandomMove(ctx.MAIN_BOARD, lastMove)
        makeMove(ctx.MAIN_BOARD, move)
        
        ctx.SOLUTION_SEQ.append(move)
        lastMove = move

    ctx.TEXT_DISPLAY = 'press arrow keys to slide' 

"""
-x---------------------------
y  
-   left to right
-   
-   top to bottom
-
-
-
-
-
"""
def getStartingBoard():
    col,row=ctx.BOARDWIDTH,ctx.BOARDHEIGHT
    board = [[]]*col
    for c in range (col):
        board[c] = [0]*row

    n=0
    for r in range(row):
        for c in range(col):
            n+=1
            board[c][r]=n
    board[col-1][row-1]=ctx.BLANK

    return board



def slideAnimation(board, direction, animationSpeed):
    x, y = getBlankPosition(board)
    if direction == ctx.UP:
        y += 1
    elif direction == ctx.DOWN:
        movex = x
        y -= 1
    elif direction == ctx.LEFT:
        x += 1
    elif direction == ctx.RIGHT:
        x -= 1

    #print(f'{movex},{movey}')
    update_screen()

    from_x, from_y = getLeftTopOfTile(x, y)
    
    for i in range(0, ctx.TILESIZE, animationSpeed):
        """
        to 'refresh' the old rect color 
        """
        pygame.draw.rect(ctx.DISPLAYSURF, ctx.BGCOLOR, (from_x, from_y, ctx.TILESIZE, ctx.TILESIZE))

        if direction == ctx.UP:
            drawTile(x, y, board[x][y], 0, -i)
        if direction == ctx.DOWN:
            drawTile(x, y, board[x][y], 0, i)
        if direction == ctx.LEFT:
            drawTile(x, y, board[x][y], -i, 0)
        if direction == ctx.RIGHT:
            drawTile(x, y, board[x][y], i, 0)

        
        pygame.display.update()
        ctx.FPSCLOCK.tick(ctx.FPS)

def update_screen():
    #screen
    ctx.DISPLAYSURF.fill(ctx.BGCOLOR)

    #check win
    if ctx.MAIN_BOARD == ctx.SOLVEDBOARD:
        #print('solved')
        ctx.TEXT_DISPLAY = 'Solved'
        #play won animation
        for tilex in range(len(ctx.MAIN_BOARD)):
            for tiley in range(len(ctx.MAIN_BOARD[0])):
                    left, top = getLeftTopOfTile(tilex, tiley)
                    pygame.draw.rect(ctx.DISPLAYSURF, ctx.BLACK, (left , top , ctx.TILESIZE, ctx.TILESIZE))
                    
                    pygame.display.update()
                    ctx.FPSCLOCK.tick(ctx.FPS)
        ctx.MAIN_BOARD=[]
        ctx.SOLVEDBOARD = None
        pygame.time.wait(1000)
        renew_game(ctx.TOTAL_NUMBER)
        ctx.SOLVEDBOARD = getStartingBoard() 
        print('renewed')
        return
        
    #show text
    textSurf, textRect = makeText(ctx.TEXT_DISPLAY, ctx.MESSAGECOLOR, ctx.BGCOLOR, 5, 5)
    ctx.DISPLAYSURF.blit(textSurf, textRect)

    board=ctx.MAIN_BOARD
    #boxes
    for col in range(ctx.BOARDWIDTH):
        for row in range(ctx.BOARDHEIGHT):
            if board[col][row]:
                drawTile(col, row, board[col][row])

    left, top = getLeftTopOfTile(0, 0)
    width = ctx.BOARDWIDTH * ctx.TILESIZE
    height = ctx.BOARDHEIGHT * ctx.TILESIZE
    pygame.draw.rect(ctx.DISPLAYSURF, ctx.BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    #buttons
    ctx.DISPLAYSURF.blit(ctx.RESET_SURF, ctx.RESET_RECT)
    ctx.DISPLAYSURF.blit(ctx.NEW_SURF, ctx.NEW_RECT)
    ctx.DISPLAYSURF.blit(ctx.SOLVE_SURF, ctx.SOLVE_RECT)

    #steps has made
    ctx.STEP_SURF =  ctx.BASICFONT.render(str(ctx.STEP_TOTAL), True, ctx.TEXTCOLOR, ctx.BGCOLOR)
    ctx.DISPLAYSURF.blit(ctx.STEP_SURF, ctx.STEP_RECT)

    pygame.display.update()
    ctx.FPSCLOCK.tick(ctx.FPS)

def makeText(text, color, bgcolor, top, left):
    textSurf = ctx.BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)



def getBlankPosition(board):
    for x in range(ctx.BOARDWIDTH):
        for y in range(ctx.BOARDHEIGHT):
            if board[x][y] == ctx.BLANK:
                return (x, y)
    raise Exception("blank board not found !!")

def terminate():
    pygame.quit()
    sys.exit()


def drawTile(x, y, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(x, y)
    pygame.draw.rect(ctx.DISPLAYSURF, ctx.TILECOLOR, (left + adjx, top + adjy, ctx.TILESIZE, ctx.TILESIZE))

    textSurf = ctx.BASICFONT.render(str(number), True, ctx.TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(ctx.TILESIZE / 2) + adjx, top + int(ctx.TILESIZE / 2) + adjy
    ctx.DISPLAYSURF.blit(textSurf, textRect)



def makeMove(board, move):
    x, y = getBlankPosition(board)
    if move == ctx.UP :
        slideAnimation(board, ctx.UP, animationSpeed=ctx.SLIDE_SPEED)
        board[x][y], board[x][y + 1] = board[x][y + 1], board[x][y]
    elif move == ctx.DOWN :
        slideAnimation(board, ctx.DOWN, animationSpeed=ctx.SLIDE_SPEED)
        board[x][y], board[x][y - 1] = board[x][y - 1], board[x][y]
    elif move == ctx.LEFT :
        slideAnimation(board, ctx.LEFT, animationSpeed=ctx.SLIDE_SPEED)
        board[x][y], board[x + 1][y] = board[x + 1][y], board[x][y]
    elif move == ctx.RIGHT :
        slideAnimation(board, ctx.RIGHT, animationSpeed=ctx.SLIDE_SPEED)
        board[x][y], board[x - 1][y] = board[x - 1][y], board[x][y]



def getLeftTopOfTile(idx_x, idx_y):
    left = ctx.XMARGIN + (idx_x * ctx.TILESIZE) + (idx_x - 1)
    top = ctx.YMARGIN + (idx_y * ctx.TILESIZE) + (idx_y - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, ctx.TILESIZE, ctx.TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == ctx.UP and blanky != ctx.BOARDHEIGHT - 1) or \
           (move == ctx.DOWN and blanky != 0) or \
           (move == ctx.LEFT and blankx != len(board) - 1) or \
           (move == ctx.RIGHT and blankx != 0)

def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [ctx.UP, ctx.DOWN, ctx.LEFT, ctx.RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == ctx.UP or not isValidMove(board, ctx.DOWN):
        validMoves.remove(ctx.DOWN)
    if lastMove == ctx.DOWN or not isValidMove(board, ctx.UP):
        validMoves.remove(ctx.UP)
    if lastMove == ctx.LEFT or not isValidMove(board, ctx.RIGHT):
        validMoves.remove(ctx.RIGHT)
    if lastMove == ctx.RIGHT or not isValidMove(board, ctx.LEFT):
        validMoves.remove(ctx.LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)

def resetAnimation(board, all_moves):
    revAllMoves = all_moves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == ctx.UP:
            oppositeMove = ctx.DOWN
        elif move == ctx.DOWN:
            oppositeMove = ctx.UP
        elif move == ctx.RIGHT:
            oppositeMove = ctx.LEFT
        elif move == ctx.LEFT:
            oppositeMove = ctx.RIGHT
        makeMove(board, oppositeMove)
        
        