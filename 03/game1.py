'''
    fill screen with bg color and display by calling flip()
'''
import sys
import pygame

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Game")

    bg_color = (230, 230, 230)
    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(bg_color)
        pygame.display.flip()

run_game()