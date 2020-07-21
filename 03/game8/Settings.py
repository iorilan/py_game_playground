class Settings():
    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.game_name = "Game"


        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 30

        
        self.fleet_drop_speed = 5
        self.reset()

        self.ship_limit = 3
        
        self.alien_points = 50
    
    def reset(self):
        self.speedup_scale = 1.1
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1 # how fast move left-right

        self.fleet_direction = 1

    def speed_up(self):
        self.ship_speed_factor, self.bullet_speed_factor, self.alien_speed_factor = \
        self.ship_speed_factor * self.speedup_scale, self.bullet_speed_factor * self.speedup_scale, \
        self.alien_speed_factor * self.speedup_scale