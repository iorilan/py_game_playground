"""
--shuffle array	
random.shuffle

--point collide with rect object
rect=pygame.Rect(left,top,width,height)
rect.collidepoint(x,y)

--draw shapes
pygame.draw.line(screen, color, (x1,y1), (x2,y2))
pygame.draw.rect(screen, color, (left, top, width, height))
pygame.draw.polygon(screen, color, ((x,y),(x,y)...))
pygame.draw.ellipse(screen, color, (left,top, length, width))


--get screen
screen= pygame.display.set_mode((ctx.WINDOW_WIDTH, ctx.WINDOW_HEIGHT))

--update background color
screen.fill(ctx.BGCOLOR)


--refresh screen
pygame.display.update()

--wait
pygame.time.Clock.tick(FPS)
pygame.time.wait(2000)
"""


import random, pygame, sys
from pygame.locals import *
from vars import game_ctx as ctx
import helper 

helper.good_to_go()

def udpate_screen():
    ctx.DISPLAY_SURF.fill(ctx.BGCOLOR)
    for bx in range(ctx.BOARD_WIDTH):
        for by in range(ctx.BOARD_HEIGHT):
            l,t = helper.leftTopCoordsOfBox(bx,by)
            if not ctx.REVEALED_BOX[bx][by]:
                pygame.draw.rect(ctx.DISPLAY_SURF, ctx.BOX_COLOR, (l,t,ctx.BOX_SIZE, ctx.BOX_SIZE))
            else:
                shape,color = helper.getShapeAndColor(ctx.MAIN_BOARD, bx,by)
                helper.drawIcon(shape, color, bx, by)


def startGameAnimation():
    coveredBoxes = helper.generateRevealedBoxesData(False)
    boxes = []
    for x in range(ctx.BOARD_WIDTH):
        for y in range(ctx.BOARD_HEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = helper.splitIntoGroupsOf(8, boxes)

    udpate_screen()
    for bg in boxGroups:
        helper.revealBoxesAnimation(ctx.MAIN_BOARD, bg)
        helper.coverBoxesAnimation(ctx.MAIN_BOARD, bg)

def gameWonAnimation():
    #print(ctx.REVEALED_BOX)
    for row in range(len(ctx.REVEALED_BOX)):
        for col in range(len(ctx.REVEALED_BOX[row])):
            left, top = helper.leftTopCoordsOfBox(row,col)
            pygame.draw.rect(ctx.DISPLAY_SURF, ctx.BLUE, (left, top, ctx.BOX_SIZE, ctx.BOX_SIZE))
            pygame.display.update()
            pygame.time.wait(500)

def handle_move(e):
    ctx.MOUSE_X,ctx.MOUSE_Y = e.pos

def handle_click(e):
    ctx.MOUSE_X,ctx.MOUSE_Y = e.pos
    boxx,boxy = helper.getBoxAtPixel(ctx.MOUSE_X, ctx.MOUSE_Y)
    if boxx is None or boxy is None:
        return

    if ctx.REVEALED_BOX[boxx][boxy]:
        return
    #print(ctx.FIRST_SELECTION)
    ctx.REVEALED_BOX[boxx][boxy] = True
    if not ctx.FIRST_SELECTION:
        ctx.FIRST_SELECTION = (boxx,boxy)
        helper.revealBoxesAnimation(ctx.MAIN_BOARD,[(boxx,boxy)])
    else:
        icon1shape,icon1color = helper.getShapeAndColor(ctx.MAIN_BOARD, ctx.FIRST_SELECTION[0], ctx.FIRST_SELECTION[1])
        icon2shape,icon2color = helper.getShapeAndColor(ctx.MAIN_BOARD, boxx, boxy)

        #print(f'{icon1shape},{icon1color},{icon2shape},{icon2color}')
        if icon1shape != icon2shape or icon1color != icon2color:
            helper.coverBoxesAnimation(ctx.MAIN_BOARD,[(ctx.FIRST_SELECTION[0],ctx.FIRST_SELECTION[1]),(boxx,boxy)])
            pygame.time.wait(1000)
            ctx.REVEALED_BOX[ctx.FIRST_SELECTION[0]][ctx.FIRST_SELECTION[1]] = False
            ctx.REVEALED_BOX[boxx][boxy]=False
        elif helper.hasWon(ctx.REVEALED_BOX):
            gameWonAnimation()
            pygame.time.wait(1000)
            
            ctx.MAIN_BOARD = helper.getRandomizedBoard()
            ctx.REVEALED_BOX = helper.generateRevealedBoxesData(False)

            udpate_screen()
            pygame.display.update()
            pygame.time.wait(2000)

            startGameAnimation()
        ctx.FIRST_SELECTION = None


def handle_event():
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif e.type == MOUSEMOTION:
            handle_move(e)

        elif e.type == MOUSEBUTTONUP:
            handle_click(e)

    boxx,boxy = helper.getBoxAtPixel(ctx.MOUSE_X, ctx.MOUSE_Y)
    if boxx != None and boxy != None:
        if not ctx.REVEALED_BOX[boxx][boxy]:
            helper.drawHighlightBox(boxx,boxy)
            shape,color = helper.getShapeAndColor(ctx.MAIN_BOARD, boxx,boxy)
            helper.draw_hint(shape, color)
    

def main():
    pygame.init()
    ctx.FPSCLOCK = pygame.time.Clock()
    ctx.DISPLAY_SURF = pygame.display.set_mode((ctx.WINDOW_WIDTH, ctx.WINDOW_HEIGHT))

    pygame.display.set_caption('Memory Game')

    ctx.MAIN_BOARD = helper.getRandomizedBoard()
    ctx.REVEALED_BOX  = helper.generateRevealedBoxesData(False)

    ctx.DISPLAY_SURF.fill(ctx.BGCOLOR)
    startGameAnimation()

    mouse_x,mouse_y,firstSelection = 0,0,None
        

    while True:
        udpate_screen()
        handle_event()
        
        pygame.display.update()
        ctx.FPSCLOCK.tick(ctx.FPS)


if __name__ == "__main__":
    main()

