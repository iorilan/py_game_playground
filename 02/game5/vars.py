
class game_ctx:
    FPSCLOCK = None
    DISPLAY_SURF = None

#config
    FPS = 30
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    REVEAL_SPEED = 8
    BOX_SIZE = 40
    GAP_SIZE = 10
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 7 
    
    X_MARGIN = 10#int((WINDOW_WIDTH - (BOARD_WIDTH*(BOX_SIZE+GAP_SIZE)))/2)
    Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT*(BOX_SIZE+GAP_SIZE)))/2)


    #shape
    DONUT = 'donut'
    SQUARE = 'square'
    DIAMOND = 'diamond'
    LINES = 'lines'
    OVAL = 'oval'
    
    ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

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

    REVEALED_BOX=None
    MAIN_BOARD=None

    MOUSE_X=0
    MOUSE_Y=0
    FIRST_SELECTION=None
    # MOUSE_ON_BOX=set()
    # MOUSE_ON_BOX_SIZE=5
