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
        self.image = pygame.Surface((15, self.game.spielfeldhoehe/9))
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
            self.rect.centery = self.game.ball.rect.centery + 10
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
        self.pos = pygame.math.Vector2(self.game.spielfeldx + self.game.spielfeldbreite/2 + 1,HEIGHT/2)
        self.direction = [random.uniform(30, 60),random.uniform(120,150),random.uniform(210,240),random.uniform(300,330)][random.randrange(0,4)]
        self.vel = pygame.math.Vector2(5, 0).rotate(self.direction)

    def update(self):
        #bewegen
        self.pos += self.vel
        self.rect.center = self.pos
        # oben und unten anstoßen
        if self.rect.top <= self.game.spielfeldy + 8:
            if self.game.debug:
                print("Oben an der Wand abrpallen")
            self.rect.top = self.game.spielfeldy + 8
            self.vel.y = -self.vel.y
            # Fliegt der Ball seitlich am Rand kann er dadruch, dass die Spieler sich nur bis zum Spielfeldrandbewegen können, festhängen. Er fliegt daher zur Seite
            if self.vel.y == 0:
                if self.game.debug:
                    print("Vertikaler Flug erkannt")
                if self.get_direction() == RIGHT:
                    self.vel = self.vel.rotate(20)
                else:
                    self.vel = self.vel.rotate(-20)
            # Ein Horizontal fliegender Ball fliegt eventuell endlos hoch und runter. Daher fliegt er zur Seite
            elif self.vel.x == 0:
                if self.game.debug:
                    print("Horizontaler Flug erkannt")
                if self.pos.x < self.game.spielfeldx + self.game.spielfeldbreite/2:
                    self.vel = self.vel.rotate(-20)
                else:
                    self.vel = self.vel.rotate(20)
            # Fliegt der Ball zu gerade nach oben dauert es ewig bis er ein Ziel erreicht. Daher fliegt er zur Seite
            else:
                if self.get_direction() == RIGHT and self.vel.x * 3 < self.vel.y:
                    if self.game.debug:
                        print("Flug zu wenig nach rechts geneigt")
                    self.vel = self.vel.rotate(-15)
                elif self.get_direction() == LEFT and - (self.vel.x * 3) < self.vel.y:
                    if self.game.debug:
                        print("Flug zu wenig nach links geneigt")
                    self.vel = self.vel.rotate(15)
        if self.rect.bottom >= self.game.spielfeldy + self.game.spielfeldhoehe - 7:
            if self.game.debug:
                print("Unten an der Wand abrpallen")
            self.rect.bottom = self.game.spielfeldy + self.game.spielfeldhoehe - 7
            self.vel.y = -self.vel.y
            # Fliegt der Ball seitlich am Rand kann er dadruch, dass die Spieler sich nur bis zum Spielfeldrandbewegen können, festhängen. Er fliegt daher zur Seite
            if self.vel.y == 0:
                if self.game.debug:
                    print("Vertikaler Flug erkannt")
                if self.get_direction() == RIGHT:
                    self.vel = self.vel.rotate(-20)
                else:
                    self.vel = self.vel.rotate(20)
            # Fliegt der Ball zu gerade nach unten dauert es ewig bis er ein Ziel erreicht. Daher fliegt er zur Seite
            elif self.vel.x == 0:
                if self.game.debug:
                    print("Horizontaler Flug erkannt")
                if self.pos.x < self.game.spielfeldx + self.game.spielfeldbreite/2:
                    self.vel = self.vel.rotate(20)
                else:
                    self.vel = self.vel.rotate(+20)
            else:
                if self.get_direction() == RIGHT and self.vel.x * 3 < -self.vel.y:
                    if self.game.debug:
                        print("Flug zu wenig nach rechts geneigt")
                    self.vel = self.vel.rotate(15)
                elif self.get_direction() == LEFT and - (self.vel.x * 3) < -self.vel.y:
                    if self.game.debug:
                        print("Flug zu wenig nach links geneigt")
                    self.vel = self.vel.rotate(-15)
        # links oder rechts rausgeflogen <- Spiel endet
        if self.rect.left < self.game.spielfeldx:
            self.game.make_game_end(1)
        if self.rect.right > self.game.spielfeldx + self.game.spielfeldbreite:
            self.game.make_game_end(0)

        # Schneller werden (in Abhängigkeit von den Schläge nach der Funktion m * x + b)
        self.vel.scale_to_length(1/8 * self.game.schläge + 5)

    def get_direction(self):
        if self.vel.x < 0:
            return LEFT
        else:
            return RIGHT

class Hindernis(pygame.sprite.Sprite):
    def __init__(self, game, pos, size):
        self._layer = 2
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(HINDERNIS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.direction = random.choice([MOVE_UP,MOVE_DOWN])
        self.speed = random.randrange(1,3)

    def update(self):
        if self.game.with_moving_hindernisse:
            if self.direction == MOVE_UP:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
            if self.rect.top <= self.game.spielfeldy + 50:
                self.direction = MOVE_DOWN
            if self.rect.bottom >= self.game.spielfeldy + self.game.spielfeldhoehe - 50:
                self.direction = MOVE_UP