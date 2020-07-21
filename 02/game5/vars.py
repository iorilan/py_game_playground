class config:
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

class color:
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

    ALL_COLORS = (color.RED, color.GREEN ,color.BLUE, color.YELLOW, color.ORANGE, color.PURPLE, color.CYAN)

class shape:
    DONUT = 'donut'
    SQUARE = 'square'
    DIAMOND = 'diamond'
    LINES = 'lines'
    OVAL = 'oval'
    
    ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

def good():
    assert (config.BOARD_WIDTH*config.BOARD_HEIGHT)%2==0, 'BOARD NEED TO HAVE AN EVEN NUM OF BOXES FOR PAIR OF MATCHES'
    assert len(color.ALL_COLORS)*len(shape.ALL_SHAPES)*2 >= config.BOARD_WIDTH*config.BOARD_HEIGHT,
    'Board is too big for # of shapes/colors defined'
    

