import pygame
from random import randrange, uniform

class Knoten:

    def __init__(self,max_speed,background):
        self.__pos = pygame.Vector2(randrange(0,background.width),randrange(0,background.height))
        self.__vel = pygame.Vector2(uniform(-max_speed,max_speed),uniform(-max_speed,max_speed))
        self.__bg = background

    def update(self):
        self.__pos += self.__vel
        if self.__pos.x < 0 or self.__pos.x > self.__bg.width:
            self.__vel.x = -self.__vel.x
        if self.__pos.y < 0 or self.__pos.y > self.__bg.height:
            self.__vel.y = -self.__vel.y

    def pos(self) -> pygame.Vector2:
        return self.__pos

class Background:

    def __init__(self,width,height,knoten_farbe,hintergrund_farbe,linienfarbe=None,anz_knoten = None,knoten_radius = 5,max_speed=10,connection_distance = 70,connection_line_width = 1):
        self.width = width
        self.height = height

        if anz_knoten is None:
            anz_knoten = int(width*height/5000)
        self.__knoten = []
        self.__max_speed = max_speed
        for knoten_num in range(anz_knoten):
            self.__knoten.append(Knoten(self.__max_speed,self))

        self.knoten_color = knoten_farbe
        self.__background_color = hintergrund_farbe
        self.__linien_color = linienfarbe
        if linienfarbe is None:
            self.__linien_color = knoten_farbe
        self.__connection_distance = connection_distance
        self.knoten_radius = knoten_radius
        self.connection_line_width = connection_line_width

        self.calculate_colors_depending_on_distance()

        self.__image = pygame.Surface((width,height))

    def calculate_colors_depending_on_distance(self):
        add_two_colors = lambda color1, color2, transparency: int((color1 * (255 - transparency) + color2 * transparency) / 255)
        connection_multiplikator = -255 / ((2 / 3) * self.__connection_distance)
        connection_addition = 255 - connection_multiplikator * (1 / 3) * self.__connection_distance
        self.__colors = {}
        for dist in range(self.__connection_distance):
            line_transparency = 255
            if dist > (1 / 3) * self.__connection_distance:
                line_transparency = connection_multiplikator * dist + connection_addition
            self.__colors[dist] = pygame.Color(add_two_colors(self.__background_color.r, self.__linien_color.r, line_transparency),
                                               add_two_colors(self.__background_color.g, self.__linien_color.g, line_transparency),
                                               add_two_colors(self.__background_color.b, self.__linien_color.b, line_transparency))

    def update(self):
        for knoten in self.__knoten:
            knoten.update()

    def draw(self) -> pygame.Surface:
        self.__image.fill(self.__background_color)
        # draw lines to other knoten
        for knoten in self.__knoten:
            for connect_knoten in self.__knoten:
                if knoten != connect_knoten:
                    distance = knoten.pos().distance_to(connect_knoten.pos())
                    if distance < self.__connection_distance:
                        pygame.draw.line(self.__image, self.__colors[int(distance)], (int(knoten.pos().x), int(knoten.pos().y)), (int(connect_knoten.pos().x), int(connect_knoten.pos().y)), self.connection_line_width)
        # draw knoten
        for knoten in self.__knoten:
            pygame.draw.circle(self.__image, self.knoten_color, (int(knoten.pos().x),int(knoten.pos().y)), self.knoten_radius)
        return self.__image

    # set sizes
    def set_size(self,width,height):
        self.width = width
        self.height = height
    def set_knoten_size(self, radius):
        self.knoten_radius = radius
    def set_line_size(self, width):
        self.connection_line_width = width

    # add or delte knoten
    def set_anz_knoten(self,neue_anzahl):
        if neue_anzahl != 0:
            if neue_anzahl < len(self.__knoten):
                del self.__knoten[randrange(0,len(self.__knoten))]
            elif neue_anzahl > len(self.__knoten):
                self.__knoten.append(Knoten(self.__max_speed,self))
    # get anzhal knoten
    def get_num_knoten(self):
        return len(self.__knoten)

    # set colors
    def set_knoten_color(self,color):
        self.knoten_color = color
    def set_background_color(self,color):
        self.__background_color = color
        self.calculate_colors_depending_on_distance()
    def set_linien_color(self,color):
        self.__linien_color = color
        self.calculate_colors_depending_on_distance()

    # set max distance where knoten are connected
    def set_connection_distance(self,distance):
        self.__connection_distance = distance
        self.calculate_colors_depending_on_distance()