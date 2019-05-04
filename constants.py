import pygame
from os import path, listdir

# Bildschrimgröße
WIDTH = 480*2
HEIGHT = 320 * 2
FPS = 60

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

# Konstanten für Art des Spielendes und die Tastenarten
START_GAME = "start"
BEFORE_FIRST_GAME = "before first game"
NEXT_GAME = "next game"
MAIN_SETTING = "main settings"

# Tasten
MOVE_UP = "move up"
MOVE_DOWN = "move down"
LEFT = "left"
RIGHT = "right"
ESC = "escape"
ALL = "all"
START = "start"
XY = "xy"
X = "x"
AB = "ab"
B = "b"

# Standartfarben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_RED = (255, 60, 60)
TEXT_GREEN = (190,220,100)
TEXT_GREY = (140,140,140)
TEXT_COLOR = (225,230,255)
SPIELFELD_FORREST = (34,139,34)
SPIELFELD_DARK = (0,100,0)
SPIELFELD_OLIVE = (105,139,34)
SPIELFELD_BLACK = (8,50,8)
PLAYER_COLOR = (200,250,200)
BALL_COLOR = (220,255,220)
MAKIERUNGEN = (120,170,100)

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')

# Lautstärke
game_music_volume = 0.2
game_sound_volume = 0.5

def load_graphics_from_file_array(file_array, dir, color_key=None, convert_aplha=False, as_dict=False):
    # Lädt alle Dateien des file_array's aus dem Pfad dir. Ein leeres file_array bedeutet alle Dateien des Pfades lesen.
    # Wenn color_key gesetzt ist wird dieser hinzugefügt.
    # Bei den Endgegner ist zudem eine alpha convert notwendig. Dazu convert_aplha auf True setzten.
    # Wenn as_dict True ist wird ein Dictionary mit Dateiname und dazu gehöriger Datei zurückgegeben.
    if file_array == []:
        file_array = [f for f in listdir(dir) if path.isfile(path.join(dir, f)) and f != '.DS_Store']

    if as_dict:
        return_images = {}
    else:
        return_images = []

    for img in file_array:
        if convert_aplha:
            loaded_img = pygame.image.load(path.join(dir, img)).convert_alpha()
        else:
            loaded_img = pygame.image.load(path.join(dir, img)).convert()

        if color_key != None:
            loaded_img.set_colorkey(color_key)
        if len(file_array) == 1:
            return loaded_img
        else:
            if as_dict:
                return_images[img] = loaded_img
            else:
                return_images.append(loaded_img)

    return return_images


# Dateipfade herausfinden
# Diese Pythondatei sollte im gleichen Ordner liegen wie der img Ornder mit den Grafiken und der snd Ordner mit den Tönen
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

background = load_graphics_from_file_array(["background.png"], img_dir)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

#pygame.mixer.music.load(path.join(snd_dir, '<name>'))
#pygame.mixer.music.set_volume(game_music_volume)
#pygame.mixer.music.play(loops=-1)