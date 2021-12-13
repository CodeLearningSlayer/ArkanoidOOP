from Game_Object import GameObject
import pygame as pg
import config as c

class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, speed, dx=0):
        super().__init__(x, y, w, h)
        self.color = color
        self.speed = speed
        self.move_left = False
        self.move_right = False
        self.dx = dx
        self.state = True
        self.dy = 0

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        if key == pg.K_LEFT:
            self.move_left = not self.move_left
        if key == pg.K_RIGHT:
            self.move_right = not self.move_right

    def change_state(self):
        self.state = False

    def downscale(self):
        self.bounds.width = 150

    def update(self):
        if self.move_left and self.left > 0 :
            self.dx = -1
        elif self.move_right and self.right < c.screen_width:
            self.dx = 1
        else:
            return
        self.move(self.dx, 0)
