
class ctx:
    
    BOARDWIDTH = 4  # number of columns in the board
    BOARDHEIGHT = 4 # number of rows in the board
    TILESIZE = 80
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    FPS = 30
    BLANK = None

    #                 R    G    B
    BLACK =         (  0,   0,   0)
    WHITE =         (255, 255, 255)
    BRIGHTBLUE =    (  0,  50, 255)
    DARKTURQUOISE = (  3,  54,  73)
    GREEN =         (  0, 204,   0)

    BGCOLOR = DARKTURQUOISE
    TILECOLOR = GREEN
    TEXTCOLOR = WHITE
    BORDERCOLOR = BRIGHTBLUE
    BASICFONTSIZE = 30

    BUTTONCOLOR = WHITE
    BUTTONTEXTCOLOR = BLACK
    MESSAGECOLOR = WHITE

    XMARGIN = 10 #int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    FPSCLOCK = None
    DISPLAYSURF= None
    BASICFONT= None
    RESET_SURF= None
    RESET_RECT= None
    NEW_SURF= None
    NEW_RECT= None
    SOLVE_SURF= None 
    SOLVE_RECT= None
    STEP_SURF=None
    STEP_RECT=None
    STEP_TOTAL=0

    MAIN_BOARD = None
    SOLUTION_SEQ = None
    SOLVEDBOARD = None

    ALL_MOVES = []
    SLIDE_TO = None

    TOTAL_NUMBER = 30
    SLIDE_SPEED=20

    TEXT_DISPLAY=''
