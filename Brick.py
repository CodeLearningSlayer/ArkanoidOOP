from Game_Object import GameObject
import pygame as pg
from config import RED, GREEN, LIGHT_BLUE, path_hit


class Brick(GameObject):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color
        self.hit_sound = pg.mixer.Sound(path_hit)
        self.hit_sound.set_volume(0.1)

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.bounds)

    def setcolor(self):
        if self.hits == 1:
            self.color = LIGHT_BLUE
        elif self.hits == 2:
            self.color = GREEN
        elif self.hits == 3:
            self.color = RED

    def hit(self):
        self.hit_sound.play()


class StrongBrick(Brick):
    color = RED
    hits = 3


class MediumBrick(Brick):
    color = GREEN
    hits = 2


class WeakBrick(Brick):
    color = LIGHT_BLUE
    hits = 1