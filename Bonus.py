from Game_Object import GameObject
import pygame as pg


class Bonus(GameObject):
    def __init__(self, x, y, w, h, speed):
        super().__init__(x, y, w, h, speed, 0, 1)
        self.speed = speed
        self.path = f"sprites/{self.__class__.__name__}.jpg"
        self.img = pg.image.load(self.path)
        self.img = pg.transform.scale(self.img,(40, 40))

    def draw(self, surface):
        surface.blit(self.img, self.bounds)

    def update(self):
        super().update()

class SmallPaddle(Bonus):
    pass


class SmallBall(Bonus):
    pass


class StickyPaddle(Bonus):
    pass
