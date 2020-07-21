import pygame
from  pygame.sprite import Sprite,Group
from Ship import Ship

class GameStats():
    def __init__(self ,setting):
        self.setting = setting
        self.reset()

        self.game_active = False
        self.score = 0
        self.highest = 0
        self.game_level = 1

    def reset(self):
        self.ships_left = self.setting.ship_limit

class Scoreboard():
    def __init__(self, setting, screen, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.setting = setting
        self.stats = stats

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

    def update_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def update_game_level(self):
        str_level = f'Level: {self.stats.game_level}'
        self.level_image = self.font.render(str_level,True, self.text_color, self.setting.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def try_update_highest(self):
        if self.stats.score > self.stats.highest:
            self.stats.highest = self.stats.score

        str_highest = str(self.stats.highest)    
        self.highest_image = self.font.render(str_highest, True, self.text_color,self.setting.bg_color)
        self.highest_rect = self.highest_image.get_rect()
        self.highest_rect.centerx = self.screen_rect.centerx
        self.highest_rect.top = self.score_rect.top

    def update_left_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            s = Ship(self.setting, self.screen)
            s.rect.left = 10 + i * s.rect.width
            s.rect.top = 10
            self.ships.add(s)

    def blit_me(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_image, self.highest_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #can do this because sprite has 'image' attribute
        self.ships.draw(self.screen)
        
            