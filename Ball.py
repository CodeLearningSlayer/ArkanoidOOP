from Game_Object import GameObject
import pygame as pg
import config as c


class Ball(GameObject):
    def __init__(self, x, y, r, color, speed, dx, dy):
        super().__init__(x-r, y-r, r*2, r*2)
        self.color = color
        self.radius = r
        self.diameter = r*2
        self.speed = speed
        self.state = False
        self.dx = 0
        self.dy = -1

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.center, self.radius)

    def handle(self, key):
        if key == pg.K_SPACE:
            self.state = True

    # def update(self):
    #     self.physics()
    #     print(self.state)
    #     if self.state:
    #         self.bounds.move(self.dx, self.dy)

    def physics(self):
        if self.centerx < self.radius or c.screen_width - self.centerx <= self.radius:
            self.dx = -self.dx
            if self.centerx < self.radius:
                self.bounds.centerx = self.radius
        if self.centery <= self.radius:
            self.dy = -self.dy

    def update(self):
        if self.state:
            super().update()
