from Game_Object import GameObject
import pygame as pg
import config as c

class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, speed):
        super().__init__(x, y, w, h)
        self.color = color
        self.speed = speed
        self.move_left = False
        self.move_right = False

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.bounds)

    def handle(self, key):
        if key == pg.K_LEFT:
            self.move_left = not self.move_left
        if key == pg.K_RIGHT:
            self.move_right = not self.move_right

    def update(self):
        if self.move_left and self.left > 0 :
            self.bounds.left -= self.speed
        elif self.move_right and self.right < c.screen_width:
            self.bounds.right += self.speed
        else:
            return
