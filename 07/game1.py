#Next can not eat own tail
#score
#eat food bug (tail reducing)

import pygame, sys
from pygame.locals import *
import random

class color:
    BLACK = (0,0,0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 128, 0)
    WHITE = (255, 255, 255)

class game_ctx:
    game_over = False
    FPSCLOCK = None
    DISPLAY_SURF = None
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BGCOLOR=color.BLACK
    FPS=30

    @staticmethod
    def init():
        game_ctx.FPSCLOCK = pygame.time.Clock()
        game_ctx.DISPLAY_SURF = pygame.display.set_mode((game_ctx.WINDOW_WIDTH, game_ctx.WINDOW_HEIGHT))
        snake.init()
        food.init()

class food:
    size=[20,20]
    color=color.YELLOW
    coord_x=[]
    coord_y=[]
    cur=[]
    @staticmethod
    def init():
        w,h=(game_ctx.WINDOW_WIDTH-50), (game_ctx.WINDOW_HEIGHT-50)
        for x in range(0, w):
            food.coord_x.append(x)
        for y in range(0, h):
            food.coord_y.append(y)
        food.cur=food.rand_food()

    @staticmethod
    def rand_food():
        f=(random.choice(food.coord_x), random.choice(food.coord_y))
        food_rect = pygame.Rect(f[0],f[1],food.size[0],food.size[1])
        for u in snake.unit:
            r = pygame.Rect(u[0],u[1],snake.size[0], snake.size[1])
            if r.colliderect(food_rect):
                return food.rand_food()
        return f

class snake:
    size=[20,20]
    color=color.ORANGE
    unit=list()
    speed=5
    dir='r'
    @staticmethod
    def init():
        left,top=(game_ctx.WINDOW_WIDTH-20)//2, (game_ctx.WINDOW_HEIGHT-20)//2
        snake.unit.append([left,top])

#https://www.pygame.org/docs/ref/key.html
def handle_event():
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        elif e.type==KEYDOWN:
            if e.key==K_LEFT and snake.dir != 'r':
                snake.dir='l'
            elif e.key==K_RIGHT and snake.dir != 'l':
                snake.dir='r'
            elif e.key==K_UP and snake.dir != 'd':
                snake.dir='u'
            elif e.key==K_DOWN and snake.dir != 'u':
                snake.dir='d'
        
def run():
    pygame.init()
    game_ctx.init()
    pygame.display.set_caption('snake game')

def check_gameover():
    x,y=snake.unit[0][0],snake.unit[0][1]
    if x<0 or x>game_ctx.WINDOW_WIDTH-snake.size[0] \
    or y < 0 or y>game_ctx.WINDOW_HEIGHT-snake.size[1]:
        game_ctx.game_over=True

def draw_snake():
    for i in range(len(snake.unit)-1,0,-1):
        snake.unit[i][0]=snake.unit[i-1][0]
        snake.unit[i][1]=snake.unit[i-1][1]

    if snake.dir=='r':
        snake.unit[0][0]+=snake.speed
    elif snake.dir=='l':
        snake.unit[0][0]-=snake.speed
    elif snake.dir=='u':
        snake.unit[0][1]-=snake.speed
    elif snake.dir=='d':
        snake.unit[0][1]+=snake.speed

    for i in range(0, len(snake.unit)):
        x,y=snake.unit[i]
        pygame.draw.rect(game_ctx.DISPLAY_SURF, snake.color,(x,y, snake.size[0], snake.size[1]))

    
def check_food():
    snake_rect = pygame.Rect(snake.unit[0][0],snake.unit[0][1],snake.size[0],snake.size[1])
    food_rect = pygame.Rect(food.cur[0],food.cur[1],food.size[0],food.size[1])
    if snake_rect.colliderect(food_rect):
        head=snake.unit[0]
        if snake.dir == 'r':
            snake.unit.insert(0, [head[0]+snake.size[0], head[1]])
        elif snake.dir == 'l':
            snake.unit.insert(0, [head[0]-snake.size[0], head[1]])
        elif snake.dir == 'u':
            snake.unit.insert(0, [head[0], head[1]-snake.size[1]])
        elif snake.dir == 'd':
            snake.unit.insert(0, [head[0], head[1]+snake.size[1]])
        food.cur = food.rand_food()
        
    pygame.draw.rect(game_ctx.DISPLAY_SURF, food.color,(food.cur[0],food.cur[1], food.size[0], food.size[1]))

def update_screen():
    #screen
    game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)
    
    draw_snake()

    check_food()

    check_gameover()

run()
while not game_ctx.game_over:
    update_screen()

    handle_event()

    pygame.display.update()
    game_ctx.FPSCLOCK.tick(game_ctx.FPS)