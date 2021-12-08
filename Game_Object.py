import pygame as pg


class GameObject:
    def __init__(self, x, y, w, h, speed=0, dx=0, dy=0):
        self.bounds = pg.Rect(x, y, w, h)
        self.speed = speed
        self.dx = dx
        self.dy = dy

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface):
        pass

    def move(self):
        self.bounds.x += self.dx * self.speed
        self.bounds.y += self.dy * self.speed

    def update(self):
        if self.dx or self.dy:
            self.move()
        else:
            return
