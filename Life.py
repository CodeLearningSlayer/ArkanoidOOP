import pygame as pg
from config import score_x

class Life:
    def __init__(self, pic_filename, coordx):
        self.__path = pic_filename
        self.__image = pg.image.load(self.__path).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (50, 50))
        self.bounds = self.__image.get_rect()
        self.coordx = coordx

    def draw(self, surface):
        surface.blit(self.__image, (self.coordx, 15))

    def update(self):
        pass
