import pygame
from pygame.locals import *

GAME_IMG = pygame.image.load('resources/image/shoot.png').convert_alpha()

BULLET_IMG = {
    'SINGLE_NORMAL': GAME_IMG.subsurface((1004, 987, 9, 21))
}

PLAYER_PLANE_IMG = [
        GAME_IMG.subsurface((0, 99, 102, 126)),
        GAME_IMG.subsurface((165, 360, 102, 126)),
        GAME_IMG.subsurface((165, 234, 102, 126)),
        GAME_IMG.subsurface((330, 624, 102, 126)),
        GAME_IMG.subsurface((330, 498, 102, 126)),
        GAME_IMG.subsurface((432, 624, 102, 126))]

ENEMY_IMG = {
    'SMALL': GAME_IMG.subsurface((534, 612, 57, 43))
}

ENEMY_EXPLODE_IMG = {
    'SMALL': [  GAME_IMG.subsurface((267, 347, 57, 43)),
                GAME_IMG.subsurface((873, 697, 57, 43)),
                GAME_IMG.subsurface((267, 296, 57, 43)),
                GAME_IMG.subsurface((930, 697, 57, 43))]
}

PLAYER_SPEED = 5

PLAYER_BULLET_SPEED = 8

ENEMY_SPEED = {
    'SMALL': 2
}

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = BULLET_IMG[bullet_type]
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_position
        self.speed = PLAYER_BULLET_SPEED

    def move(self):
        self.rect.top -= self.speed



class Player(pygame.sprite.Sprite):
    def __init__(self, init_position):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       self.image = PLAYER_PLANE_IMG
       self.rect = self.image[0].get_rect()
       self.rect.topleft = init_position
       self.speed = PLAYER_SPEED
       self.bullets = pygame.sprite.Group()
       self.img_index = 0
       self.got_hit = False

    def shoot(self, bullet_type):
        bullet = Bullet(bullet_type, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def moveDown(self):
        self.rect.bottom += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def moveLeft(self):
        self.rect.left -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0

    def moveRight(self):
        self.rect.right += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = ENEMY_IMG[enemy_type]
        self.explode_image = ENEMY_EXPLODE_IMG[enemy_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = ENEMY_SPEED[enemy_type]

    def move(self):
        self.rect.top += self.speed
