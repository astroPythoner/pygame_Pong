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
SELECT = "select"
XY = "xy"
X = "x"
Y = "y"
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
HINDERNIS_COLOR = (130,255,130)
LONG_POWER_UP_COLOR =    (155,35,35)
SCHUTZ_POWER_UP_COLOR =  (195,45,45)
LANGSAM_POWER_UP_COLOR = (235,55,55)
BAD_LONG_POWER_UP_COLOR =    (55,55,160)
BAD_SCHUTZ_POWER_UP_COLOR =  (65,65,190)
BAD_LANGSAM_POWER_UP_COLOR = (75,75,220)

# POWER_UPS
LONG_POWER_UP = "long power up"
SCHUTZ_POWER_UP = "schutz power up"
LANGSAM_POWER_UP = "langsam power up"
POWER_UPS = {LONG_POWER_UP:[LONG_POWER_UP_COLOR,BAD_LONG_POWER_UP_COLOR],SCHUTZ_POWER_UP:[SCHUTZ_POWER_UP_COLOR,BAD_SCHUTZ_POWER_UP_COLOR],LANGSAM_POWER_UP:[LANGSAM_POWER_UP_COLOR,BAD_LANGSAM_POWER_UP_COLOR]}

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

LANGSAM_POWER_UP_img = load_graphics_from_file_array(["small turtle.png"], img_dir, color_key=BLACK)
SCHUTZ_POWER_UP_img = load_graphics_from_file_array(["small schild.png"], img_dir, color_key=BLACK)
LONG_POWER_UP_img = load_graphics_from_file_array(["small pfeile.png"], img_dir, color_key=BLACK)

pong_sound = pygame.mixer.Sound(path.join(snd_dir, 'ping_pong_8bit_beeep.ogg'))
pong_sound.set_volume(game_sound_volume)
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
power_sound.set_volume(game_sound_volume * 0.5)
#pygame.mixer.music.load(path.join(snd_dir, '<name>'))
#pygame.mixer.music.set_volume(game_music_volume)
#pygame.mixer.music.play(loops=-1)