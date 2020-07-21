import random, pygame, sys
from pygame.locals import *

#config
FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH*(BOX_SIZE+GAP_SIZE)))/2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT*(BOX_SIZE+GAP_SIZE)))/2)

#color
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255,0 ,255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHT_BGCOLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

ALL_COLORS = (RED, GREEN ,BLUE, YELLOW, ORANGE, PURPLE, CYAN)

# shape
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


assert (BOARD_WIDTH*BOARD_HEIGHT)%2==0, 'BOARD NEED TO HAVE AN EVEN NUM OF BOXES FOR PAIR OF MATCHES'
assert len(ALL_COLORS)*len(ALL_SHAPES)*2 >= BOARD_WIDTH*BOARD_HEIGHT,'Board is too big for # of shapes/colors defined'

def main():
    global FPSCLOCK , DISPLAY_SURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    DISPLAY_SURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAY_SURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for e in pygame.event.get():
            if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEMOTION:
                mousex,mousey = e.pos
            elif e.type == MOUSEBUTTONUP:
                mousex,mousey = e.pos
                mouseClicked = True
        boxx,boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard,[(boxx,boxy)]) # tuple+array ?
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None:
                    firstSelection = (boxx,boxy)
                else:
                    icon1shape,icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape,icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy]=False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    firstSelection = None
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape,color))

    random.shuffle(icons)
    numIconUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:numIconUsed]*2
    random.shuffle(icons)

    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    res = []
    for i in range(0, len(theList), groupSize):
        res.append(theList[i:i+groupSize])
    return res

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOX_SIZE + GAP_SIZE)+X_MARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE)+Y_MARGIN

    return (left,top)

def getBoxAtPixel(x, y):
    for bx in range(BOARD_WIDTH):
        for by in range(BOARD_HEIGHT):
            l,t = leftTopCoordsOfBox(bx,by)
            rect = pygame.Rect(l,t,BOX_SIZE,BOX_SIZE)
            if rect.collidepoint(x,y):
                return (bx,by)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOX_SIZE * 0.25)
    half = int (BOX_SIZE * 0.25)

    left,top = leftTopCoordsOfBox(boxx, boxy)
    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left+half, top+half), half-5)
        pygame.draw.circle(DISPLAY_SURF, BGCOLOR, (left+half, top+half), quarter-5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left+quarter, top+quarter, BOX_SIZE-half, BOX_SIZE-half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, (
                                                (left+BOX_SIZE-1,top+half), 
                                                (left+half, top+BOX_SIZE-1),
                                                (left,top+half)
                                                ))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAY_SURF, color, (left,top+i), (left+i, top))
            pygame.draw.line(DISPLAY_SURF, color, (left+i, top+BOX_SIZE-1),(left+BOX_SIZE-1,top+i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left,top+quarter, BOX_SIZE, half))

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
        shape,color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left,top,coverage,BOX_SIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED)-1, -REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for c in range(0, BOX_SIZE+ REVEAL_SPEED, REVEAL_SPEED):
        drawBoxCovers(board, boxesToCover, c)

def drawBoard(board, revealed):
    for bx in range(BOARD_WIDTH):
        for by in range(BOARD_HEIGHT):
            l,t = leftTopCoordsOfBox(bx,by)
            if not revealed[bx][by]:
                pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (l,t,BOX_SIZE, BOX_SIZE))
            else:
                shape,color = getShapeAndColor(board, bx,by)
                drawIcon(shape, color, bx, by)

def drawHighlightBox(bx, by):
    l,t = leftTopCoordsOfBox(bx,by)
    pygame.draw.rect(DISPLAY_SURF, HIGHLIGHT_COLOR, (l-5,t-5, BOX_SIZE+10, BOX_SIZE+10), 4)

def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for bg in boxGroups:
        revealBoxesAnimation(board, bg)
        coverBoxesAnimation(board, bg)
    
def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHT_BGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1 ,color2 = color2,color1
        DISPLAY_SURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == "__main__":
    main()

