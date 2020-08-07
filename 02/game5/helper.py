
import random, pygame, sys
from pygame.locals import *
from vars import game_ctx as ctx

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (ctx.BOX_SIZE + ctx.GAP_SIZE)+ctx.X_MARGIN
    top = boxy * (ctx.BOX_SIZE + ctx.GAP_SIZE)+ctx.Y_MARGIN

    return (left,top)

def splitIntoGroupsOf(groupSize, theList):
    res = []
    for i in range(0, len(theList), groupSize):
        res.append(theList[i:i+groupSize])
    return res

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(ctx.BOARD_WIDTH):
        revealedBoxes.append([val] * ctx.BOARD_HEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    icons = []
    for color in ctx.ALL_COLORS:
        for shape in ctx.ALL_SHAPES:
            icons.append((shape,color))

    random.shuffle(icons)
    numIconUsed = int(ctx.BOARD_WIDTH * ctx.BOARD_HEIGHT / 2)
    icons = icons[:numIconUsed]*2
    random.shuffle(icons)

    board = []
    for x in range(ctx.BOARD_WIDTH):
        column = []
        for y in range(ctx.BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    #print(board)
    return board


def getBoxAtPixel(x, y):
    for bx in range(ctx.BOARD_WIDTH):
        for by in range(ctx.BOARD_HEIGHT):
            l,t = leftTopCoordsOfBox(bx,by)
            rect = pygame.Rect(l,t,ctx.BOX_SIZE,ctx.BOX_SIZE)
            """
                if (x,y) in this rect
            """
            if rect.collidepoint(x,y):
                return (bx,by)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(ctx.BOX_SIZE * 0.25)
    half = int (ctx.BOX_SIZE * 0.25)

    left,top = leftTopCoordsOfBox(boxx, boxy)
    #print(left,top)
    if shape == ctx.DONUT:
        pygame.draw.line(ctx.DISPLAY_SURF, color, (left,top), (left+ctx.BOX_SIZE, top+ctx.BOX_SIZE))
        pygame.draw.line(ctx.DISPLAY_SURF, color, (left+ctx.BOX_SIZE,top), (left, top+ctx.BOX_SIZE))
    elif shape == ctx.SQUARE:
        pygame.draw.rect(ctx.DISPLAY_SURF, color, (left+quarter, top+quarter, ctx.BOX_SIZE-half, ctx.BOX_SIZE-half))
    elif shape == ctx.DIAMOND:
        pygame.draw.polygon(ctx.DISPLAY_SURF, color, (
                                                (left+ctx.BOX_SIZE-1,top+half), 
                                                (left+half, top+ctx.BOX_SIZE-1),
                                                (left,top+half)
                                                ))
    elif shape == ctx.LINES:
        for i in range(0, ctx.BOX_SIZE, 4):
            pygame.draw.line(ctx.DISPLAY_SURF, color, (left,top+i), (left+i, top))
            pygame.draw.line(ctx.DISPLAY_SURF, color, (left+i, top+ctx.BOX_SIZE-1),(left+ctx.BOX_SIZE-1,top+i))
    elif shape == ctx.OVAL:
        pygame.draw.ellipse(ctx.DISPLAY_SURF, color, (left,top+quarter, ctx.BOX_SIZE, half))

def draw_hint(shape, color):
    x,y= ctx.BOARD_WIDTH,1
    drawIcon(shape, color, x,y)

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(ctx.DISPLAY_SURF, ctx.BGCOLOR, (left, top, ctx.BOX_SIZE, ctx.BOX_SIZE))
        shape,color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(ctx.DISPLAY_SURF, ctx.BOX_COLOR, (left,top,coverage,ctx.BOX_SIZE))
    pygame.display.update()
    ctx.FPSCLOCK.tick(ctx.FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(ctx.BOX_SIZE, (-ctx.REVEAL_SPEED)-1, -ctx.REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for c in range(0, ctx.BOX_SIZE+ ctx.REVEAL_SPEED, ctx.REVEAL_SPEED):
        drawBoxCovers(board, boxesToCover, c)

def drawHighlightBox(bx, by):
    l,t = leftTopCoordsOfBox(bx,by)
    pygame.draw.rect(ctx.DISPLAY_SURF, ctx.HIGHLIGHT_COLOR, (l-5,t-5, ctx.BOX_SIZE+10, ctx.BOX_SIZE+10), 4)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


def good_to_go():
    assert (ctx.BOARD_WIDTH*ctx.BOARD_HEIGHT)%2==0, 'BOARD NEED TO HAVE AN EVEN NUM OF BOXES FOR PAIR OF MATCHES'
    assert len(ctx.ALL_COLORS)*len(ctx.ALL_SHAPES)*2 >= ctx.BOARD_WIDTH*ctx.BOARD_HEIGHT,'Board is too big for # of shapes/colors defined'

