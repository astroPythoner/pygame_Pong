import pygame
from constants import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, player_num, is_computer = False):
        self._layer = 1
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
        # Merken, wie oft der Spieler schon geschossen hat
        self.schläge = 0
        self.is_long = False
        # Schutzschild des Spielers nach einsammeln des Power-Ups
        self.schild = None

    def update(self):
        # Bewegen
        if self.is_computer:
            self.rect.centery = self.game.ball.rect.centery
        else:
            if not self.game.multi_on_one:
                if self.game.check_key_pressed(MOVE_UP, self.player_num):
                    self.rect.y -= (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
                elif self.game.check_key_pressed(MOVE_DOWN, self.player_num):
                    self.rect.y += (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
            else:
                if self.player_num == 0:
                    if self.game.check_key_pressed(MOVE_UP, 0):
                        self.rect.y -= (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
                    elif self.game.check_key_pressed(MOVE_DOWN, 0):
                        self.rect.y += (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
                elif self.player_num == 1:
                    if self.game.check_key_pressed(X, 0):
                        self.rect.y -= (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
                    elif self.game.check_key_pressed(B, 0):
                        self.rect.y += (self.game.spielfeldhoehe / 80) * self.game.time_diff * FPS
        if self.rect.top < self.game.spielfeldy+8:
            self.rect.top = self.game.spielfeldy+8
        if self.rect.bottom > self.game.spielfeldy + self.game.spielfeldhoehe - 7:
            self.rect.bottom = self.game.spielfeldy + self.game.spielfeldhoehe - 7

    def start_long_power_up(self):
        self.is_long = True
        # PowerUp Zeit merken
        gemerkte_pos = self.rect.center
        # Rechteck
        self.image = pygame.Surface((15, (self.game.spielfeldhoehe / 9) * 1.5))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # positionieren
        self.rect.center = gemerkte_pos

    def end_long_power_up(self):
        self.is_long = False
        gemerkte_pos = self.rect.center
        # Rechteck
        self.image = pygame.Surface((15, (self.game.spielfeldhoehe / 9)))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # positionieren
        self.rect.center = gemerkte_pos

class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = 2
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        # Rechteck
        self.image = pygame.Surface((12, 12))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        # Positionieren und Bewegung
        self.pos = pygame.math.Vector2(self.game.spielfeldx + self.game.spielfeldbreite/2 + 1,HEIGHT/2)
        self.direction = [random.uniform(30, 60),random.uniform(120,150),random.uniform(210,240),random.uniform(300,330)][random.randrange(0,4)]
        self.ball_speed = game.ball_speed
        self.vel = pygame.math.Vector2(self.ball_speed, 0).rotate(self.direction)
        # Power-Up
        self.is_power_up = False

    def update(self):
        #bewegen
        for bewegung_num in range (1,5):
            if self.game.game_status == None:
                self.pos.x += (self.vel.x * self.game.time_diff * FPS) / 4
                self.pos.y += (self.vel.y * self.game.time_diff * FPS) / 4
                self.rect.center = self.pos
                # oben und unten anstoßen
                if self.rect.top <= self.game.spielfeldy + 8:
                    if self.game.debug:
                        print("Oben an der Wand abrpallen (vel:", self.vel,")")
                    self.rect.top = self.game.spielfeldy + 9
                    self.pos.y = self.rect.centery
                    self.vel.y = -self.vel.y
                    # Pong-Sound abspielen
                    pong_sound.play()
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
                        print("Unten an der Wand abrpallen (vel:", self.vel,")")
                    self.rect.bottom = self.game.spielfeldy + self.game.spielfeldhoehe - 8
                    self.pos.y = self.rect.centery
                    self.vel.y = -self.vel.y
                    # Pong-Sound abspielen
                    self.game.play_pong_sound()
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
                    if self.game.debug:
                        print("Ball links herausgeflogen, Spieler 2 gewinnt")
                    self.game.make_game_end(1)
                if self.rect.right > self.game.spielfeldx + self.game.spielfeldbreite:
                    if self.game.debug:
                        print("Ball rechts herausgeflogen, Spieler 1 gewinnt")
                    self.game.make_game_end(0)

                self.game.detect_and_react_collisions()

                if not self.is_power_up:
                    # Schneller werden (in Abhängigkeit von den Schläge nach der Funktion m * x + b)
                    self.vel.scale_to_length(1/16 * self.game.schläge + self.ball_speed)

    def get_direction(self):
        if self.vel.x < 0:
            return LEFT
        else:
            return RIGHT

    def start_slow_power_up(self):
        self.is_power_up = True
        self.vel.scale_to_length(1 / 16 * self.game.schläge + self.ball_speed*4/3)

    def start_fast_power_up(self):
        self.is_power_up = True
        self.vel.scale_to_length(1 / 16 * self.game.schläge + self.ball_speed*2/3)

    def end_slow_power_up(self):
        self.is_power_up = False
        self.vel.scale_to_length(1 / 16 * self.game.schläge + self.ball_speed)

class Hindernis(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, is_schutz = False, geschützter_spieler = None):
        self._layer = 1
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(HINDERNIS_COLOR)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.direction = random.choice([MOVE_UP,MOVE_DOWN])
        self.speed = random.randrange(4,8) / 4
        self.is_power_type = False
        self.good_or_bad = True  # True = good  False = bad
        self.is_schutz = is_schutz
        if self.is_schutz:
            self.geschützter_spieler = geschützter_spieler

    def update(self):
        if self.game.with_moving_hindernisse and not self.is_schutz:
            if self.direction == MOVE_UP:
                self.rect.y -= self.speed * self.game.time_diff * FPS
            else:
                self.rect.y += self.speed * self.game.time_diff  * FPS
            if self.rect.top <= self.game.spielfeldy + 50:
                self.direction = MOVE_DOWN
            if self.rect.bottom >= self.game.spielfeldy + self.game.spielfeldhoehe - 50:
                self.direction = MOVE_UP

    def kill_schutz(self):
        if self.is_schutz:
            if self.geschützter_spieler == self.game.player0:
                self.game.player0_has_schutz = False
            else:
                self.game.player1_has_schutz = False
            self.kill()

    def make_to_power_up(self, power_up_type, good_or_bad):
        self.is_power_type = power_up_type
        self.good_or_bad = good_or_bad
        # Mit entsprechender Fabre füllen
        self.image.fill(POWER_UPS[power_up_type][[True,False].index(good_or_bad)])
        # Power-Up Symbol zeichnen
        if power_up_type == LANGSAM_POWER_UP:
            self.image.blit(pygame.transform.scale(LANGSAM_POWER_UP_img, (min(self.image.get_size()), min(self.image.get_size()))), (self.image.get_width()/2 - min(self.image.get_size())/2, self.image.get_height()/2 - min(self.image.get_size())/2));
        if power_up_type == SCHUTZ_POWER_UP:
            self.image.blit(pygame.transform.scale(SCHUTZ_POWER_UP_img, (min(self.image.get_size()), min(self.image.get_size()))), (self.image.get_width()/2 - min(self.image.get_size())/2, self.image.get_height()/2 - min(self.image.get_size())/2));
        if power_up_type == LONG_POWER_UP:
            self.image.blit(pygame.transform.scale(LONG_POWER_UP_img, (min(self.image.get_size()), min(self.image.get_size()))), (self.image.get_width()/2 - min(self.image.get_size())/2, self.image.get_height()/2 - min(self.image.get_size())/2));

    def remove_from_power_up(self):
        self.is_power_type = False
        self.image.fill(HINDERNIS_COLOR)