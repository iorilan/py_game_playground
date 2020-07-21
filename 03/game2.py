'''
    handle event in pygame.event.get():
'''
import sys
import pygame

class Settings():
    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230.230)
        self.game_name = "Game"

def run_game():
    pygame.init()
    setting = Settings()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption(setting.game_name)

    bg_color = (230, 230, 230)
    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(bg_color)
        pygame.display.flip()

run_game()



