import pygame
from joystickpins import JoystickPins, KeyboardStick
from constants import *
from sprites import *
import time

class Game():
    def __init__(self):
        self.game_status = START_GAME
        self.running = True
        screen.blit(background, background_rect)

        # Kontroller und Multiplayer
        self.multiplayer = False
        self.multi_on_one = False
        self.all_joysticks = []
        self.find_josticks()

        # Größe des Spielfeldes
        self.spielfeldbreite = WIDTH * 5/7
        self.spielfeldhoehe = WIDTH * 5/7 / 1.4142156
        self.spielfeld_color = SPIELFELD_DARK
        # Position des Spielfeldes
        self.spielfeld_rect = None
        self.set_spielfeldwerte()

        # Variablen für die Hindernisse
        self.with_hindernissen = True
        self.with_moving_hindernisse = True

        # Für den Computerspieler
        self.computer_difficulty = 5

        # Wie viele Schläge die Powerups aktiv sind
        self.POWERUP_TIME = 2
        # Merken wer zuletzt geschlagen hat um herauszubekommen wer ein Power-Up bekommt
        self.last_schlag = None
        # Für das Schutz Power Up
        self.player0_has_schutz = False
        self.player1_has_schutz = False

        # Runde und Gewinne beider Seiten
        self.spiel_num = 0
        self.player0_wins = 0
        self.player1_wins = 0

        # Erreichtes
        self.schläge = 0  # Zählt hoch, wie oft der Ball von den Spielern zurückgeschossen wurde

        # Debug gibt einige Prints aus und setzt an Abprallpunkte einen Sprite
        self.debug = True
        self.abprallort = None

        self.time_diff = 0

    def set_spielfeldwerte(self):
        querkant = False
        if self.spielfeldbreite >= WIDTH * 5/7:
            querkant = True
        if querkant:
            self.spielfeldx = 0
            self.spielfeldy = int((HEIGHT - self.spielfeldhoehe) / 2)
        else:
            self.spielfeldx = int((WIDTH * 5/7 - self.spielfeldbreite) / 2)
            self.spielfeldy = 0
        self.spielfeldx += 20
        self.spielfeld_rect = pygame.Rect(self.spielfeldx, self.spielfeldy, self.spielfeldbreite, self.spielfeldhoehe)

    def find_josticks(self):
        # Knöpfe und Kontroller finden und Initialisieren
        self.all_joysticks = [JoystickPins(KeyboardStick())]
        for joy in range(pygame.joystick.get_count()):
            pygame_joystick = pygame.joystick.Joystick(joy)
            pygame_joystick.init()
            my_joystick = JoystickPins(pygame_joystick)
            self.all_joysticks.append(my_joystick)
            print("found_joystick: " + my_joystick.get_name())

    def draw_text(self, surf, text, size, x, y, color=TEXT_COLOR, rect_place="oben_mitte"):
        # Zeichnet den text in der color auf die surf.
        # x und y sind die Koordinaten des Punktes rect_place. rect_place kann "oben_mitte", "oben_links" oder "oben_rechts" sein.
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if rect_place == "oben_mitte":
            text_rect.midtop = (x, y)
        elif rect_place == "oben_links":
            text_rect.x = x
            text_rect.y = y
        elif rect_place == "oben_rechts":
            text_rect.topright = (x, y)
        elif rect_place == "mitte":
            text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def check_key_pressed(self, check_for=ALL, joystick_num="both"):
        # Überprüft ob die Taste(n) check_for gedrückt ist und achtet dabei auch auf Multi und Singleplayer.
        # Bei Multiplayer kann mit joystick_num zusätzlich mitgegeben werden welcher Kontroller gemeint ist.
        if self.multiplayer:
            if joystick_num == "both":
                for joystick in self.all_joysticks:
                    if check_for == LEFT:
                        if joystick.get_axis_left() or joystick.get_shoulder_left():
                            return True
                    if check_for == RIGHT:
                        if joystick.get_axis_right() or joystick.get_shoulder_right():
                            return True
                    if check_for == MOVE_UP:
                        if joystick.get_axis_up():
                            return True
                    if check_for == MOVE_DOWN:
                        if joystick.get_axis_down():
                            return True
                    if check_for == ESC:
                        if joystick.get_select() and joystick.get_start():
                            return True
                    if check_for == START:
                        if joystick.get_start():
                            return True
                    if check_for == ALL:
                        if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                            return True
                    if check_for == XY:
                        if joystick.get_X() or joystick.get_Y():
                            return True
                    if check_for == AB:
                        if joystick.get_A() or joystick.get_B():
                            return True
                    if check_for == X:
                        if joystick.get_X():
                            return True
                    if check_for == B:
                        if joystick.get_B():
                            return True
            else:
                if check_for == LEFT:
                    if self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_shoulder_right():
                        return True
                if check_for == MOVE_UP:
                    if self.all_joysticks[joystick_num].get_axis_up():
                        return True
                if check_for == MOVE_DOWN:
                    if self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == ESC:
                    if self.all_joysticks[joystick_num].get_select() and self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == START:
                    if self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == ALL:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B() or self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y()\
                        or self.all_joysticks[joystick_num].get_start() or self.all_joysticks[joystick_num].get_shoulder_left() or self.all_joysticks[joystick_num].get_shoulder_right() \
                        or self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_axis_up() \
                        or self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == XY:
                    if self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y():
                        return True
                if check_for == AB:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B():
                        return True
                if check_for == X:
                    if self.all_joysticks[joystick_num].get_X():
                        return True
                if check_for == B:
                    if self.all_joysticks[joystick_num].get_B():
                        return True
        else:
            for joystick in self.all_joysticks:
                if check_for == LEFT:
                    if joystick.get_axis_left() or joystick.get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if joystick.get_axis_right() or joystick.get_shoulder_right():
                        return True
                if check_for == MOVE_UP:
                    if joystick.get_axis_up():
                        return True
                if check_for == MOVE_DOWN:
                    if joystick.get_axis_down():
                        return True
                if check_for == ESC:
                    if joystick.get_select() and joystick.get_start():
                        return True
                if check_for == START:
                    if joystick.get_start():
                        return True
                if check_for == ALL:
                    if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                        return True
                if check_for == XY:
                    if joystick.get_X() or joystick.get_Y():
                        return True
                if check_for == AB:
                    if joystick.get_A() or joystick.get_B():
                        return True
                if check_for == X:
                    if joystick.get_X():
                        return True
                if check_for == B:
                    if joystick.get_B():
                        return True
        return False

    def wait_for_single_multiplayer_selection(self):
        # Am Anfang, vor dem Spiel, wird zwischen Single und Multiplayer ausgewählt.
        # Links und Rechts wird zum Auswahl ändern benutzt, A oder B zum auswählen. Esc zum Spiel beenden
        self.find_josticks()
        selected = 0
        waiting = True
        last_switch = pygame.time.get_ticks()
        while waiting:
            clock.tick(FPS)
            self.show_multi_select_or_joy_select_on_screen(screen, self.game_status, selected)
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern durch hochzählen von selected
            if self.check_key_pressed(LEFT) or self.check_key_pressed(MOVE_UP):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected -= 1
                    if selected < 0:
                        selected = 0
            if self.check_key_pressed(RIGHT) or self.check_key_pressed(MOVE_DOWN):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected += 1
                    if selected > 2:
                        selected = 2
            # Auswahl getroffen
            if self.check_key_pressed(AB):
                # Single-palyer
                if selected == 0:
                    # Auswählen welcher Kontroller genommen werden soll, wenn Auswahl gepasst hat Spiel starten, sonst nochmals nach Kontrollern suchen und wieder zwischen Multi- und Singelplayer wählen lassen
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = False
                        self.multi_on_one = False
                # Multi-palyer
                elif selected == 1:
                    # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 2):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True
                        self.multi_on_one = False
                elif selected == 2:
                    # Auswählen welcher Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True
                        self.multi_on_one = True

    def wait_for_joystick_confirm(self, surf, num_joysticks):
        # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
        # num_joysticks ist die Anzahl der zu wählenden Joysticks
        # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
        # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen

        # Angeschlossene Kontroller finden
        self.find_josticks()

        # Auswahlbilschrimanzeigen
        self.show_multi_select_or_joy_select_on_screen(surf, None)
        self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
        for controller in self.all_joysticks:
            self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
        pygame.display.flip()
        # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
        time.sleep(0.5)

        # Auswahl starten
        selected_controllers = []
        selected_controller_num = 0
        last_switch = pygame.time.get_ticks()
        while len(selected_controllers) < num_joysticks:
            clock.tick(FPS)
            # Bildschrimzeichnen
            self.show_multi_select_or_joy_select_on_screen(surf, None)
            self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
            # Jeden gefundenen Kontroller zut Auswahl stellen
            for controller in self.all_joysticks:
                if self.all_joysticks.index(controller) == selected_controller_num:
                    self.draw_text(surf, controller.get_name(), 30, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts", color=TEXT_RED)
                else:
                    self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
                if controller in selected_controllers:
                    self.draw_text(surf, "bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), color=TEXT_GREEN, rect_place="oben_links")
                else:
                    self.draw_text(surf, "nicht bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), rect_place="oben_links")
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern
            if (self.check_key_pressed(LEFT) or self.check_key_pressed(MOVE_UP)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num -= 1
                if selected_controller_num < 0:
                    selected_controller_num = 0
            if (self.check_key_pressed(RIGHT) or self.check_key_pressed(MOVE_DOWN)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num += 1
                if selected_controller_num >= len(self.all_joysticks):
                    selected_controller_num = len(self.all_joysticks) - 1
            # Auswahl getroffen
            if self.check_key_pressed(AB):
                if self.all_joysticks[selected_controller_num] not in selected_controllers:
                    selected_controllers.append(self.all_joysticks[selected_controller_num])
            # Zurück zur Multi- / Singleplayer auswahl
            if self.check_key_pressed(XY):
                return False
        # Wenn genug Kontroller gewählt wurden stimmt die Auswahl. Es wrid True zurückgegeben
        if len(selected_controllers) == num_joysticks:
            self.all_joysticks = selected_controllers
            return True
        # Wenn die Auswahl nicht stimmt wird False zurückgegeben
        else:
            return False

    def settings(self,surf):
        # Mithilfe dieser Funktion kann der Spieler die Einstellungen, sprich Spielfeldgröße oder Farben, ändern

        # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
        time.sleep(0.5)

        # Auswahl starten
        selected_row = 0
        if self.multiplayer:
            selected_row = 1
        selected_colum = 1
        last_switch = pygame.time.get_ticks()

        while True:

            clock.tick(FPS)
            # Bildschrimzeichnen
            self.show_einstellungen_on_screen(surf, selected_row,selected_colum)
            pygame.display.flip()

            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()

            # Auswahl ändern
            if self.check_key_pressed(MOVE_UP) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_row -= 1
                if not self.multiplayer:
                    if selected_row < 0:
                        selected_row = 0
                else:
                    if selected_row < 1:
                        selected_row = 1
                if selected_row <= 1:
                    if selected_colum >= 2:
                        selected_colum = 2
                    else:
                        selected_colum = 1
            if self.check_key_pressed(MOVE_DOWN)and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_row += 1
                if selected_row > 3:
                    selected_row = 3
            if self.check_key_pressed(AB) and last_switch + 200 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected_row == 1:
                    if selected_colum == 1:
                        if self.with_hindernissen:
                            self.with_hindernissen = False
                        else:
                            self.with_hindernissen = True
                    else:
                        if self.with_moving_hindernisse:
                            self.with_moving_hindernisse = False
                        else:
                            self.with_moving_hindernisse = True
                if selected_row == 2:
                    self.spielfeldhoehe  = [HEIGHT     , min(WIDTH*5/7,HEIGHT), WIDTH * 5/7 / 1.4142156, WIDTH * 5/7 / 2][selected_colum]
                    self.spielfeldbreite = [WIDTH * 5/7, min(WIDTH*5/7,HEIGHT), WIDTH * 5/7            , WIDTH * 5/7    ][selected_colum]
                if selected_row == 3:
                    self.spielfeld_color = [SPIELFELD_FORREST,SPIELFELD_DARK,SPIELFELD_OLIVE,SPIELFELD_BLACK][selected_colum]
                self.set_spielfeldwerte()
            if self.check_key_pressed(LEFT) and last_switch + 200 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected_row == 0:
                    self.computer_difficulty -= 1
                    if self.computer_difficulty < 0:
                        self.computer_difficulty = 0
                else:
                    selected_colum -= 1
                    if selected_row == 1:
                        if selected_colum < 1:
                            selected_colum = 1
                    else:
                        if selected_colum < 0:
                            selected_colum = 0
            if self.check_key_pressed(RIGHT) and last_switch + 200 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                if selected_row == 0:
                    self.computer_difficulty += 1
                    if self.computer_difficulty > 10:
                        self.computer_difficulty = 10
                else:
                    selected_colum += 1
                    if selected_row == 1:
                        if selected_colum > 2:
                            selected_colum = 2
                    else:
                        if selected_colum > 3:
                            selected_colum = 3
            if self.check_key_pressed(START):
                return

    def show_einstellungen_on_screen(self,surf,selected_row, selected_column):
        screen.blit(background, background_rect)

        # Texte
        if not self.multiplayer:
            if selected_row == 0:
                self.draw_text(surf, "Schwierigkeit: " + str(self.computer_difficulty), 34, WIDTH / 2, HEIGHT * 2/5 - 90, color=TEXT_RED, rect_place="mitte")
            else:
                self.draw_text(surf, "Schwierigkeit: " + str(self.computer_difficulty), 34, WIDTH / 2, HEIGHT * 2/5 - 90, color=TEXT_COLOR, rect_place="mitte")
        else:
            self.draw_text(surf, "Schwierigkeit nur im Singleplayer", 28, WIDTH / 2, HEIGHT * 2 / 5 - 90, color=TEXT_GREY, rect_place="mitte")

        hindernis_texte = []
        if self.with_hindernissen:
            hindernis_texte.append("Mit Hindernissen")
        else:
            hindernis_texte.append("Ohne Hindernisse")
        if self.with_moving_hindernisse:
            hindernis_texte.append("Hindernisse bewegen sich")
        else:
            hindernis_texte.append("Hindernisse stehen still")
        for num, text in enumerate(hindernis_texte):
            if selected_row == 1 and selected_column == num+1:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-180,180][num], HEIGHT * 2/5 - 30, color=TEXT_RED, rect_place="mitte")
            else:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-180,180][num], HEIGHT * 2/5 - 30, color=TEXT_COLOR, rect_place="mitte")

        for num, text in enumerate(["Vollbild","Quadtratisch","Rechteck","Langgestreckt"]):
            if selected_row == 2 and selected_column == num:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 30, color=TEXT_RED, rect_place="mitte")
            elif self.spielfeldhoehe == [HEIGHT, min(WIDTH*5/7,HEIGHT), WIDTH * 5/7 / 1.4142156, WIDTH * 5/7 / 2][num] and self.spielfeldbreite == [WIDTH * 5/7, min(WIDTH*5/7,HEIGHT), WIDTH * 5/7, WIDTH * 5/7][num]:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 30, color=TEXT_GREEN, rect_place="mitte")
            else:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 30, color=TEXT_COLOR, rect_place="mitte")
        for num, text in enumerate(["Waldgrün","Dunkelgrün","Olivgrün","Schwarz"]):
            if selected_row == 3 and selected_column == num:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 90, color=TEXT_RED, rect_place="mitte")
            elif self.spielfeld_color == [SPIELFELD_FORREST,SPIELFELD_DARK,SPIELFELD_OLIVE,SPIELFELD_BLACK][num]:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 90, color=TEXT_GREEN, rect_place="mitte")
            else:
                self.draw_text(surf, text, 34, WIDTH / 2 + [-300,-100,100,300][num], HEIGHT * 2/5 + 90, color=TEXT_COLOR, rect_place="mitte")

        # Texte unten mit Hinweisen zur Bedienung
        self.draw_text(surf, "W/S oder Joystick zum Auswahl ändern", 20, WIDTH / 2, HEIGHT * 3 / 4 - 25)
        if selected_row == 1:
            self.draw_text(surf, "Pfeiltasten oder A/B zum Auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
        else:
            self.draw_text(surf, "A/D oder Joystick zum erhöhen oder verringern", 20, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)

    def show_multi_select_or_joy_select_on_screen(self, surf, calling_reason, selected=None):
        screen.blit(background, background_rect)

        # Je nach dem ob es um die Kontrollerauswahl oder die Einstellungen geht ein anderen Text zeigen
        if calling_reason == START_GAME:
            texte = ["Single player","Multi player","Multiplayer auf einen Kontroller"]
        else:
            texte = []

        for text_num in range(0,len(texte)):
            if text_num == selected:
                self.draw_text(surf, texte[text_num], 34, WIDTH/2, HEIGHT/2 + (40*text_num), color=TEXT_RED, rect_place="mitte")
            else:
                self.draw_text(surf, texte[text_num], 25, WIDTH/2, HEIGHT/2 + (40*text_num), rect_place="mitte")

        # Standart Texte
        self.draw_text(surf, "PONG!", 64, WIDTH / 2, HEIGHT / 6.5)
        self.draw_text(surf, "Der Klassiker: Pong!", 32, WIDTH / 2, HEIGHT / 2.8)
        self.draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum Auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)

    def show_game_info(self, surf, center_x,center_y = HEIGHT*3/5):
        if self.game_status == None:
            self.draw_text(surf, "PONG!", 64, center_x, HEIGHT / 6.5)
        self.draw_text(surf, "Runde: {}".format(self.spiel_num), 25, center_x, center_y - 80)
        self.draw_text(surf, "Spieler 1", 30, center_x, center_y - 30)
        self.draw_text(surf, "Spieler 2", 30, center_x, center_y + 50)
        self.draw_text(surf, str(self.player0_wins), 30, center_x, center_y + 10)
        self.draw_text(surf, str(self.player1_wins), 30, center_x, center_y + 90)
        self.draw_text(surf, "Schläge: "+str(self.schläge), 25, center_x, center_y + 150)

    def draw_power_up_info(self, center_x, y):
        rechteck = pygame.Rect(center_x - 90, y, 25, 25)
        pygame.draw.rect(screen, LONG_POWER_UP_COLOR, rechteck)
        screen.blit(pygame.transform.scale(LONG_POWER_UP_img, (24, 24)), (center_x - 90, y))
        self.draw_text(screen,"-> Größerer Spieler",20,center_x-55,y,rect_place="oben_links")
        rechteck = pygame.Rect(center_x - 90, y + 40, 25, 25)
        pygame.draw.rect(screen, LANGSAM_POWER_UP_COLOR, rechteck)
        screen.blit(pygame.transform.scale(LANGSAM_POWER_UP_img, (24, 24)), (center_x - 90, y + 40))
        self.draw_text(screen,"-> Langsamer Ball",20,center_x-55,y+40,rect_place="oben_links")
        rechteck = pygame.Rect(center_x - 90, y + 80, 25, 25)
        pygame.draw.rect(screen, SCHUTZ_POWER_UP_COLOR, rechteck)
        screen.blit(pygame.transform.scale(SCHUTZ_POWER_UP_img, (24, 24)), (center_x - 90, y + 80))
        self.draw_text(screen,"-> Schutzwand",20,center_x-55,y+80,rect_place="oben_links")

    def show_end_game_info(self, surf, center_x, y, gewonnener_spieler = None):
        if self.game_status == NEXT_GAME:
            if gewonnener_spieler == None:
                self.draw_text(surf, "Abgebrochen", 50, center_x, y + 70)
            elif gewonnener_spieler == 0:
                self.draw_text(surf, "Spieler 1 gewinnt", 50, center_x, y + 70)
            elif gewonnener_spieler == 1:
                self.draw_text(surf, "Spieler 2 gewinnt", 50, center_x, y + 70)
        if not self.game_status == BEFORE_FIRST_GAME:
            self.draw_text(surf, "Start zum Nochmalspielen", 20, center_x, y + 185)
            self.draw_text(surf, "X/Y für Einstellungen", 20, center_x, y + 215)
        else:
            self.draw_text(surf, "Start drücken um loszuspielen", 50, center_x, y + 120)
            self.draw_text(surf, "X/Y oder Pfeiltasten für Einstellungen", 50, center_x, y + 200)
        self.show_game_info(surf,center_x)

        pygame.display.flip()
        time.sleep(0.5)

        waiting = True
        while waiting:
            clock.tick(FPS)
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # mit Start geht's weiter
            if self.check_key_pressed(START):
                waiting = False
            if self.check_key_pressed(XY):
                self.settings(screen)
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            if self.game_status == NEXT_GAME:
                if gewonnener_spieler == None:
                    self.draw_text(surf, "Abgebrochen", 50, center_x, y + 70)
                elif gewonnener_spieler == 0:
                    self.draw_text(surf, "Spieler 1 gewinnt", 50, center_x, y + 70)
                elif gewonnener_spieler == 1:
                    self.draw_text(surf, "Spieler 2 gewinnt", 50, center_x, y + 70)
            if not self.game_status == BEFORE_FIRST_GAME:
                self.draw_text(surf, "Start zum Nochmalspielen", 20, center_x, y + 185)
                self.draw_text(surf, "X/Y für Einstellungen", 20, center_x, y + 215)
            else:
                self.draw_text(surf, "Start drücken um loszuspielen", 50, center_x, y + 120)
                self.draw_text(surf, "X/Y oder Pfeiltasten für Einstellungen", 50, center_x, y + 200)

        self.game_status = NEXT_GAME

    ########## Hier startet das eigentliche Spiel ##########
    def start_game(self):
        # Multiplayerauswahl
        self.wait_for_single_multiplayer_selection()
        self.game_status = BEFORE_FIRST_GAME
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        self.show_end_game_info(screen, WIDTH / 2, 20)
        self.game_status = START_GAME

        # Dauerschleife des Spiels
        while self.running:
            # Ist das Spiel aus irgendeinem Grund zu Ende, ist also game_over nicht None, werden alle Spieler, Gegner und Meteoriten erstellt und das Spiel gestartet
            if self.game_status == NEXT_GAME or self.game_status == START_GAME:
                self.new()

            # Bilschirm leeren
            screen.fill(BLACK)
            screen.blit(background, background_rect)

            # Auf Bildschirmgeschwindigkeit achten
            self.time_diff = clock.tick(FPS) / 1000

            # Eingaben zum Verlassen des Spiels checken
            if self.check_key_pressed(ESC):
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Spiel abbrechen
            if self.check_key_pressed(X):
                self.make_game_end(None)

            # Bewegungen berechnen
            self.all_sprites.update()

            # Kolissionen checken
            self.detect_and_react_collisions()

            # Skalen und Texte auf den Bildschirm malen
            self.draw_display()
            self.all_sprites.draw(screen)

            # Im Debug letzten Abprallort zeichnen
            if self.debug and self.abprallort is not None:
                pygame.draw.rect(screen, TEXT_RED, pygame.Rect(self.abprallort[0] - 3, self.abprallort[1] - 3, 7, 7))

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.alles_abprallende = pygame.sprite.Group()
        self.hindernisse = pygame.sprite.Group()

        # neues Spielfeld
        self.set_spielfeldwerte()

        # Spieler erstellen
        self.player0 = Player(self, 0)
        if self.multiplayer:
            self.player1 = Player(self, 1)
        else:
            self.player1 = Player(self, 1, is_computer=True)
        self.all_sprites.add(self.player0)
        self.all_sprites.add(self.player1)
        self.alles_abprallende.add(self.player0)
        self.alles_abprallende.add(self.player1)

        # Wenn so eingestellt Hindernisse erzeugen
        if self.with_hindernissen:
            if not self.with_moving_hindernisse:
                start_time = time.time() * 1000
                used_positions = []
                placed_hindernise = 0
                while placed_hindernise < 7:
                    x = random.randrange(int(self.spielfeldx + 150), int(self.spielfeldx + self.spielfeldbreite - 150))
                    y = random.randrange(int(self.spielfeldy + 90), int(self.spielfeldy + self.spielfeldhoehe - 90))
                    if (x,y) not in used_positions:
                        placed_hindernise += 1
                        width = random.randrange(40, int(self.spielfeldbreite/8))
                        height = random.randrange(30, int(self.spielfeldhoehe/8))
                        hindernis = Hindernis(self, (x, y), (width, height))
                        self.hindernisse.add(hindernis)
                        self.all_sprites.add(hindernis)
                        self.alles_abprallende.add(hindernis)
                        for x_pos in range(-width-30,width+30):
                            for y_pos in range(-height-30,height+30):
                                used_positions.append((x_pos+x,y_pos+y))
                    if start_time + 1000 < time.time() * 1000:
                        print("not found")
                        break
            else:
                for num in range(0,7):
                    x = self.spielfeldx + (self.spielfeldbreite * (num+2)/10) + random.randrange(-10,10)
                    y = random.randrange(int(self.spielfeldy + 100), int(self.spielfeldy+self.spielfeldhoehe - 100))
                    width = random.randrange(30,45)
                    height = random.randrange(30,int(self.spielfeldhoehe/6.5))
                    hindernis = Hindernis(self,(x,y),(width,height))
                    self.hindernisse.add(hindernis)
                    self.all_sprites.add(hindernis)
                    self.alles_abprallende.add(hindernis)

        # Ball erstellen
        self.ball = Ball(self)
        self.all_sprites.add(self.ball)

        # Spielwerte zurücksetzten
        self.game_status = None
        self.schläge = 0
        self.abprallort = None
        self.last_schlag = None
        self.player0_has_schutz = False
        self.player1_has_schutz = False

    def detect_and_react_collisions(self):
        # Überprüfen ob der Ball irgendwo abprallen soll
        for hindernis in self.alles_abprallende:
            hit = pygame.sprite.collide_rect(self.ball,hindernis)
            if hit:
                if self.debug: # Position des Abpralls für den Debug merken
                    self.abprallort = self.ball.rect.center
                # Wenn von einem Spieler abgeprallt wurde anzahl der Schläge hochzählen und letzten Schlag dem Spieler zuweisen
                if hindernis in [self.player0,self.player1]:
                    if self.schläge == 0 and self.with_hindernissen:
                        # Beim ersten Schuss Power-Ups platzieren
                        erstes_hindernis = random.choice(self.hindernisse.sprites())
                        erstes_hindernis.make_to_power_up(list(POWER_UPS.keys())[0])
                        while True:
                            zweites_hindernis = random.choice(self.hindernisse.sprites())
                            if zweites_hindernis != erstes_hindernis:
                                zweites_hindernis.make_to_power_up(list(POWER_UPS.keys())[1])
                                break
                        while True:
                            drittes_hindernis = random.choice(self.hindernisse.sprites())
                            if drittes_hindernis != erstes_hindernis and drittes_hindernis != zweites_hindernis:
                                drittes_hindernis.make_to_power_up(list(POWER_UPS.keys())[2])
                                break
                    # Schläge hochzählen
                    self.schläge += 1
                    if hindernis == self.player0:
                        self.player0.schläge += 1
                        self.last_schlag = self.player0
                    else:
                        self.player1.schläge += 1
                        self.last_schlag = self.player1
                # Wude von einem Hindernis abgeprallt überprüfen ob es ein Power-Up Hindernis war
                elif hindernis.is_power_type != False:
                    # Dem Spieler das Power up geben
                    if hindernis.is_power_type == LONG_POWER_UP:
                        self.last_schlag.start_long_power_up()
                    elif hindernis.is_power_type == LANGSAM_POWER_UP:
                        self.ball.start_slow_power_up()
                    elif hindernis.is_power_type == SCHUTZ_POWER_UP:
                        if (self.last_schlag == self.player0 and self.player0_has_schutz == False) or (self.last_schlag == self.player1 and self.player1_has_schutz == False):
                            # Schutzschild erstellen
                            schutz = Hindernis(self, (int(self.spielfeldx + [50,self.spielfeldbreite-50][[self.player0,self.player1].index(self.last_schlag)]), random.randrange(int(self.spielfeldy + 80), int(self.spielfeldy + self.spielfeldhoehe - 80))), (16, self.spielfeldhoehe/5), is_schutz=True, geschützter_spieler=self.last_schlag)
                            self.all_sprites.add(schutz)
                            self.alles_abprallende.add(schutz)
                            # merken das der Spieler ein Schutzschild hat
                            if self.last_schlag == self.player0:
                                self.player0_has_schutz = True
                            else:
                                self.player1_has_schutz = True
                    # Ein anderes Hindernis das noch kein PowerUp ist zu dem Power Up machen
                    while True:
                        zufälliges_hindernis = random.choice(self.hindernisse.sprites())
                        if zufälliges_hindernis.is_power_type == False and zufälliges_hindernis != hindernis:
                            zufälliges_hindernis.make_to_power_up(hindernis.is_power_type)
                            break
                    # Hindernis nichtmehr als Powerup machen
                    hindernis.remove_from_power_up()

                # Bewegung ändern     # Um zu verhindern, dass ein Ball Beispielsweise zwischen zwei Hindernissen unedlich ang hin und her fliegt wird die Flugbahn mit einem Zufallswert etwas gedreht
                if self.ball.pos.y - self.ball.vel.y > hindernis.rect.bottom and self.ball.vel.y < 0: # von unten dagegen
                    self.ball.pos.y = hindernis.rect.bottom + 6
                    self.ball.vel.y = -self.ball.vel.y
                    self.ball.vel.rotate(random.randrange(-3, 3))
                    if self.debug:
                        print("von unten")
                elif self.ball.pos.y - self.ball.vel.y < hindernis.rect.top and self.ball.vel.y > 0: # von oben dagegen
                    self.ball.pos.y = hindernis.rect.top - 6
                    self.ball.vel.y = -self.ball.vel.y
                    self.ball.vel.rotate(random.randrange(-3, 3))
                    if self.debug:
                        print("von oben")
                if self.ball.pos.x - self.ball.vel.x < hindernis.rect.left and self.ball.vel.x > 0: # von links dagegen
                    self.ball.pos.x = hindernis.rect.left - 6
                    self.ball.vel.x = -self.ball.vel.x
                    self.ball.vel.rotate(random.randrange(-3, 3))
                    if self.debug:
                        print("von links")
                elif self.ball.pos.x - self.ball.vel.x > hindernis.rect.right and self.ball.vel.x < 0: # von rechts dagegen
                    self.ball.pos.x = hindernis.rect.right + 6
                    self.ball.vel.x = -self.ball.vel.x
                    self.ball.vel.rotate(random.randrange(-3, 3))
                    if self.debug:
                        print("von rechts")

    def draw_display(self):
        # Bildschrim zeichnen

        # Hintergund des Spielfeldes Zeichnen
        pygame.draw.rect(screen, self.spielfeld_color, self.spielfeld_rect)
        # Außenumrahmung zeichnen
        pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx,                         self.spielfeldy + 3),                     (self.spielfeldx+self.spielfeldbreite,    self.spielfeldy + 3),                     8)
        pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx+self.spielfeldbreite - 4,self.spielfeldy),                         (self.spielfeldx+self.spielfeldbreite - 4,self.spielfeldy+self.spielfeldhoehe),     8)
        pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx+self.spielfeldbreite,    self.spielfeldy+self.spielfeldhoehe - 4), (self.spielfeldx,                         self.spielfeldy+self.spielfeldhoehe - 4), 8)
        pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx + 3,                     self.spielfeldy+self.spielfeldhoehe),     (self.spielfeldx + 3,                     self.spielfeldy),                         8)
        # Gestrichelte Mittellinie zeichnen
        line_num = -1
        while True:
            line_num += 1
            if line_num*20 + 10 > self.spielfeldhoehe:
                pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx + self.spielfeldbreite / 2, self.spielfeldy + line_num * 20),(self.spielfeldx + self.spielfeldbreite / 2, self.spielfeldy + self.spielfeldhoehe), 8)
                break
            else:
                pygame.draw.line(screen, MAKIERUNGEN, (self.spielfeldx + self.spielfeldbreite / 2, self.spielfeldy + line_num * 20),(self.spielfeldx + self.spielfeldbreite / 2, self.spielfeldy + line_num * 20 + 10), 8)

        # Auf der Rechten Seite noch die Info zum Spiel
        self.show_game_info(screen,WIDTH*6/7+10)
        self.draw_power_up_info(WIDTH*6/7+10, 180)

    def make_game_end(self, gewonnener_spieler=None):
        self.game_status = NEXT_GAME
        self.spiel_num += 1
        screen.blit(background, background_rect)
        if gewonnener_spieler == 0:
            self.player0_wins += 1
        elif gewonnener_spieler == 1:
            self.player1_wins += 1
        self.show_end_game_info(screen,WIDTH/2,20,gewonnener_spieler)

game = Game()
game.start_game()

pygame.quit()