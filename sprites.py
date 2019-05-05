import pygame
from constants import *
import random
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, game, player_num, is_computer = False):
        self._layer = 2
        self.game = game
        self.player_num = player_num
        self.is_computer = is_computer
        pygame.sprite.Sprite.__init__(self)
        # Rechteck
        self.image = pygame.Surface((15, 55))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # positionieren
        if self.player_num == 0:
            self.rect.left = self.game.spielfeldx + 12
        else:
            self.rect.right = self.game.spielfeldx + self.game.spielfeldbreite - 12
        self.rect.centery = HEIGHT/2

    def update(self):
        if self.is_computer:
            self.rect.centery = self.game.ball.rect.centery
        else:
            if self.game.check_key_pressed(MOVE_UP, self.player_num):
                self.rect.y -= self.game.spielfeldhoehe / 50
            elif self.game.check_key_pressed(MOVE_DOWN, self.player_num):
                self.rect.y += self.game.spielfeldhoehe / 50
        if self.rect.top < self.game.spielfeldy+8:
            self.rect.top = self.game.spielfeldy+8
        if self.rect.bottom > self.game.spielfeldy + self.game.spielfeldhoehe - 7:
            self.rect.bottom = self.game.spielfeldy + self.game.spielfeldhoehe - 7

class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = 2
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 12))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2([self.game.spielfeldx + self.game.spielfeldbreite/2 + 1,HEIGHT/2])
        self.direction = [random.uniform(30, 60),random.uniform(120,150),random.uniform(210,240),random.uniform(300,330)][random.randrange(0,4)]
        self.vel = pygame.math.Vector2(8, 0).rotate(self.direction)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if self.rect.top < self.game.spielfeldy + 8:
            self.rect.top = self.game.spielfeldy + 8
            self.vel.y = -self.vel.y
            # Fliegt der Ball zu gerade nach oben dauert es ewig bis er ein Ziel erreicht. Daher fliegt er zur Seite
            if self.get_direction() == RIGHT and self.vel.x * 3 < self.vel.y:
                self.vel = self.vel.rotate(-15)
            elif self.get_direction() == LEFT and - (self.vel.x * 3) < self.vel.y:
                self.vel = self.vel.rotate(15)
        if self.rect.bottom > self.game.spielfeldy + self.game.spielfeldhoehe - 7:
            self.rect.bottom = self.game.spielfeldy + self.game.spielfeldhoehe - 7
            self.vel.y = -self.vel.y
            # Fliegt der Ball zu gerade nach unten dauert es ewig bis er ein Ziel erreicht. Daher fliegt er zur Seite
            if self.get_direction() == RIGHT and self.vel.x * 3 < -self.vel.y:
                self.vel = self.vel.rotate(15)
            elif self.get_direction() == LEFT and - (self.vel.x * 3) < -self.vel.y:
                self.vel = self.vel.rotate(-15)
        if self.rect.left < self.game.spielfeldx:
            self.game.make_game_end(1)
        if self.rect.right > self.game.spielfeldx + self.game.spielfeldbreite:
            self.game.make_game_end(0)

    def get_direction(self):
        if self.vel.x < 0:
            return LEFT
        else:
            return RIGHT