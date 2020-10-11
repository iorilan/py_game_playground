import pygame, sys
from pygame.locals import *
from vars import color, game_ctx, bar,ball, brick_mat

#https://www.pygame.org/docs/ref/key.html
def handle_event():
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYUP and e.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        elif e.type==KEYDOWN:
            if e.key == K_LEFT:
                bar.moving_left = True
            elif e.key == K_RIGHT:
                bar.moving_right = True
        elif e.type==KEYUP:
            if e.key==K_LEFT:
                bar.moving_left=False
            elif e.key == K_RIGHT:
                bar.moving_right=False
        # elif e.type == MOUSEMOTION:
        #     pass
        # elif e.type == MOUSEBUTTONUP:
        #     pass

def run():
    pygame.init()
    game_ctx.init()
    brick_mat.init()
    pygame.display.set_caption('bouncing ball')

def check_gameover():
    if ball.y>game_ctx.WINDOW_HEIGHT-ball.size[1]//2:
        game_ctx.game_over=True
    
    #TODO check win

def draw_matrix():
    rect=[]
    for r in range(0, brick_mat.row):
        for c in range(0, brick_mat.col):
            if not brick_mat.matrix[r][c]:
                continue
            x,y=brick_mat.matrix[r][c]
            r1=pygame.draw.rect(game_ctx.DISPLAY_SURF, brick_mat.color, (x,y,brick_mat.size[0], brick_mat.size[1]))
            rect.append((r1,r,c))
    return rect
def update_screen():
    #screen
    game_ctx.DISPLAY_SURF.fill(game_ctx.BGCOLOR)

    #bar
    if bar.moving_left:
        bar.move(-bar.speed)
    elif bar.moving_right:
        bar.move(bar.speed)
    bar_rect=pygame.draw.rect(game_ctx.DISPLAY_SURF, bar.color,(bar.x, bar.y, bar.size[0], bar.size[1]))

    

    #moving ball
    ball_rect=pygame.draw.ellipse(game_ctx.DISPLAY_SURF, ball.color, (ball.x, ball.y, ball.size[0], ball.size[1]))
    x,y=ball.x,ball.y
    if x < 0 or x >= game_ctx.WINDOW_WIDTH-ball.size[0]:
        ball.speed_x=-ball.speed_x
    #ball touched bar
    if y < 0 or ball_rect.colliderect(bar_rect):
        ball.speed_y=-ball.speed_y
    ball.x+=ball.speed_x
    ball.y+=ball.speed_y

    #bricks
    bricks=draw_matrix()
    #ball touched brick
    for b,x,y in bricks:
        if b.colliderect(ball_rect):
            ball.speed_y=-ball.speed_y
            # invert x 
            if ball.y<brick_mat.matrix[x][y][1]:
                ball.speed_x=-ball.speed_x

            brick_mat.matrix[x][y]=None

    check_gameover()
    

run()
while not game_ctx.game_over:
    update_screen()

    handle_event()

    pygame.display.update()
    game_ctx.FPSCLOCK.tick(game_ctx.FPS)