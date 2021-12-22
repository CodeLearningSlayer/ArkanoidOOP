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

    def change_state(self):
        self.state = not self.state

    def handle(self, key):
        if key == pg.K_SPACE:
            self.state = True

    def physics(self):
        if self.centerx < self.radius or c.screen_width - self.centerx <= self.radius:
            self.dx = -self.dx
            if self.centerx < self.radius:
                self.bounds.centerx = self.radius
            if c.screen_width - self.centerx < self.radius:
                self.bounds.centerx = c.screen_width - self.radius
        if self.centery <= self.radius:
            self.dy = -self.dy
        self.move(self.dx, self.dy)

    def downscale(self):
        self.bounds.width = self.bounds.width // 2
        self.bounds.height = self.bounds.height // 2
        self.radius = 10

    def set_position(self, *coords):
        self.state = False
        self.bounds.centerx = coords[0]
        self.bounds.centery = coords[1]


    def update(self):
        if self.state:
            self.physics()
            super().update()
