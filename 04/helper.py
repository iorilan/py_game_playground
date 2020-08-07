import pygame, sys, random
from pygame.locals import *
from game_context import ctx



def initialize():
    ctx.FPSCLOCK = pygame.time.Clock()
    ctx.DISPLAYSURF = pygame.display.set_mode((ctx.WINDOWWIDTH, ctx.WINDOWHEIGHT))
    ctx.BASICFONT = pygame.font.Font('freesansbold.ttf', ctx.BASICFONTSIZE)

    offset_x=180
    offset_y=270
    # Store the option buttons and their rectangles in OPTIONS.
    ctx.RESET_SURF, ctx.RESET_RECT = makeText('Reset',    ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y)
    ctx.NEW_SURF,   ctx.NEW_RECT   = makeText('New Game', ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y-70)
    ctx.SOLVE_SURF, ctx.SOLVE_RECT = makeText('Solve',    ctx.TEXTCOLOR, ctx.TILECOLOR, ctx.WINDOWWIDTH - offset_x, ctx.WINDOWHEIGHT - offset_y-140)

    renew_game(ctx.TOTAL_NUMBER)
    ctx.SOLVEDBOARD = getStartingBoard() 


def renew_game(numSlides):
    ctx.SOLUTION_SEQ = []
    ctx.MAIN_BOARD = getStartingBoard()
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(ctx.MAIN_BOARD, lastMove)
        makeMove(ctx.MAIN_BOARD, move)
        
        ctx.SOLUTION_SEQ.append(move)
        lastMove = move


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(ctx.BOARDWIDTH):
        column = []
        for y in range(ctx.BOARDHEIGHT):
            column.append(counter)
            counter += ctx.BOARDWIDTH
        board.append(column)
        counter -= ctx.BOARDWIDTH * (ctx.BOARDHEIGHT - 1) + ctx.BOARDWIDTH - 1

    board[ctx.BOARDWIDTH-1][ctx.BOARDHEIGHT-1] = ctx.BLANK
    return board



def slideAnimation(board, direction, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == ctx.UP:
        movex = blankx
        movey = blanky + 1
    elif direction == ctx.DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == ctx.LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == ctx.RIGHT:
        movex = blankx - 1
        movey = blanky

    print(f'{movex},{movey}')
    update_screen()
    # prepare the base surface
    baseSurf = ctx.DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, ctx.BGCOLOR, (moveLeft, moveTop, ctx.TILESIZE, ctx.TILESIZE))
    
    for i in range(0, ctx.TILESIZE, animationSpeed):
        ctx.DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == ctx.UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == ctx.DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == ctx.LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == ctx.RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)


        pygame.display.update()
        ctx.FPSCLOCK.tick(ctx.FPS)



def update_screen():
    #screen
    ctx.DISPLAYSURF.fill(ctx.BGCOLOR)

    #message box
    message = 'Click tile or press arrow keys to slide.' 

    if ctx.MAIN_BOARD == ctx.SOLVEDBOARD:
        print('solved')
        message = 'Solved'
        #play won animation
        for tilex in range(len(ctx.MAIN_BOARD)):
            for tiley in range(len(ctx.MAIN_BOARD[0])):
                    left, top = getLeftTopOfTile(tilex, tiley)
                    pygame.draw.rect(ctx.DISPLAYSURF, ctx.BLACK, (left , top , ctx.TILESIZE, ctx.TILESIZE))
                    
                    pygame.display.update()
                    ctx.FPSCLOCK.tick(ctx.FPS)
        ctx.MAIN_BOARD=[]
        ctx.SOLVEDBOARD = None
        pygame.time.wait(500)
        renew_game(ctx.TOTAL_NUMBER)
        ctx.SOLVEDBOARD = getStartingBoard() 
        print('renewed')
        return
        
    textSurf, textRect = makeText(message, ctx.MESSAGECOLOR, ctx.BGCOLOR, 5, 5)
    ctx.DISPLAYSURF.blit(textSurf, textRect)

    board=ctx.MAIN_BOARD
    #boxes
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = ctx.BOARDWIDTH * ctx.TILESIZE
    height = ctx.BOARDHEIGHT * ctx.TILESIZE
    pygame.draw.rect(ctx.DISPLAYSURF, ctx.BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    #buttons
    ctx.DISPLAYSURF.blit(ctx.RESET_SURF, ctx.RESET_RECT)
    ctx.DISPLAYSURF.blit(ctx.NEW_SURF, ctx.NEW_RECT)
    ctx.DISPLAYSURF.blit(ctx.SOLVE_SURF, ctx.SOLVE_RECT)

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


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(ctx.DISPLAYSURF, ctx.TILECOLOR, (left + adjx, top + adjy, ctx.TILESIZE, ctx.TILESIZE))
    textSurf = ctx.BASICFONT.render(str(number), True, ctx.TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(ctx.TILESIZE / 2) + adjx, top + int(ctx.TILESIZE / 2) + adjy
    ctx.DISPLAYSURF.blit(textSurf, textRect)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == ctx.UP :
        slideAnimation(board, ctx.UP, animationSpeed=int(ctx.TILESIZE / 2))
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == ctx.DOWN :
        slideAnimation(board, ctx.DOWN, animationSpeed=int(ctx.TILESIZE / 2))
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == ctx.LEFT :
        slideAnimation(board, ctx.LEFT, animationSpeed=int(ctx.TILESIZE / 2))
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == ctx.RIGHT :
        slideAnimation(board, ctx.RIGHT, animationSpeed=int(ctx.TILESIZE / 2))
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]



def getLeftTopOfTile(tileX, tileY):
    left = ctx.XMARGIN + (tileX * ctx.TILESIZE) + (tileX - 1)
    top = ctx.YMARGIN + (tileY * ctx.TILESIZE) + (tileY - 1)
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
    return (move == ctx.UP and blanky != len(board[0]) - 1) or \
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
        
        