import pygame
import random
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)

        self.rect = self.surf.get_rect()
        self.step = 15

    def update(self, k):
        #print(k)
        if k[K_UP] and self.rect.top>0:
            self.rect.move_ip(0,-self.step)
            #_move_up_sound.play()
        if k[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0,self.step)
            #_move_down_sound.play()
        if k[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.step,0)
        if k[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.step,0)

class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.rect = self.surf.get_rect(
            center = (
                random.randint(WIDTH+20,WIDTH+100),
                random.randint(0,HEIGHT)
            )
        )
        self.speed = random.randint(1,2)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH+20,WIDTH+100),
                random.randint(0,HEIGHT)
            )
        )
    
    def update(self):
        self.rect.move_ip(-1,0)
        if self.rect.right < 0:
            self.kill()


WIDTH = 1000
HEIGHT = 800

ADD_ENEMY = pygame.USEREVENT+1
pygame.time.set_timer(ADD_ENEMY, 250)
ADD_CLOUD = pygame.USEREVENT+2
pygame.time.set_timer(ADD_CLOUD,1000)

_screen = pygame.display.set_mode([WIDTH,HEIGHT])

_player = Player()
_enemies = pygame.sprite.Group()
_all_sprites = pygame.sprite.Group()
_all_sprites.add(_player)
_clouds = pygame.sprite.Group()
_running=True
_clock = pygame.time.Clock()

#sound
pygame.mixer.init()
pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.play(loops=-1)

"""
_move_up_sound = pygame.mixer.Sound("up.ogg")
_move_down_sound = pygame.mixer.Sound("down.ogg")
_collision_sound = pygame.mixer.Sound("collision.ogg")
"""

pygame.init()



while _running:

    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                _running = False
        elif e.type == QUIT:
            _running=False
        #...more events
        elif e.type == ADD_ENEMY:
            enemy = Enemy()
            _enemies.add(enemy)
            _all_sprites.add(enemy)
        elif e.type == ADD_CLOUD:
            cloud = Cloud()
            _clouds.add(cloud)
            _all_sprites.add(cloud)

    pressed_keys = pygame.key.get_pressed()
    _clouds.update()
    _player.update(pressed_keys)
    _enemies.update()
    

    _screen.fill((135,206,250))

    for obj in _all_sprites:
        _screen.blit(obj.surf, obj.rect)
    
    if pygame.sprite.spritecollideany(_player, _enemies):
        _player.kill()
        
        """
        _move_up_sound.stop()
        _move_down_sound.stop()
        _collision_sound.play()
        """
        
        _running = False


    pygame.display.flip()

    _clock.tick(20)
pygame.quit()





