import pygame as pg
import time
from Game import Game
from Ball import Ball
from Paddle import Paddle
from Brick import StrongBrick, MediumBrick, WeakBrick, Brick
from Text_object import TextObject
import config as c
from Life import Life
import sys
import random


class Breakout(Game):
    def __init__(self, caption, width, height, bg_img_filename, frame_rate, bg_music_filename):
        super().__init__(caption, width, height, bg_img_filename, frame_rate)
        pg.mixer.music.load(bg_music_filename)
        pg.mixer.music.play(-1, 0, 5000)
        pg.mixer.music.set_volume(0.1)
        self.gamemode = True
        self.paddle = None
        self.ball = None
        self.width = width
        self.height = height
        self.points =0
        self.bricks = None
        self.score = None
        self.create_objects()
        self.life = None

    def create_paddle(self):
        self.paddle = Paddle(c.screen_width//2 - c.paddle_width//2, c.screen_height - c.paddle_height * 2,
                             c.paddle_width, c.paddle_height, c.paddle_color, c.paddle_speed)
        self.keydown_handlers[pg.K_LEFT].append(self.paddle.handle)
        self.keydown_handlers[pg.K_RIGHT].append(self.paddle.handle)
        self.keyup_handlers[pg.K_LEFT].append(self.paddle.handle)
        self.keyup_handlers[pg.K_RIGHT].append(self.paddle.handle)
        self.objects.append(self.paddle)

    def create_ball(self):
        self.ball = Ball(self.paddle.centerx, self.paddle.top - c.ball_radius,
                         c.ball_radius, c.ball_color, c.ball_speed, c.ball_dx, c.ball_dy)  # поставить по центру ракетки
        self.objects.append(self.ball)
        self.keydown_handlers[pg.K_SPACE].append(self.ball.handle)

    def create_bricks(self):
        bricks_weight = [[random.randint(0, 100) for j in range(c.screen_width//c.brick_width)] for i in range(3)]
        bricks = []
        deltax = 0
        deltay = 0
        for i in range(3):
            bufmas = []
            deltax = 10
            deltay += 2
            for j in range(c.screen_width // c.brick_width):
                if bricks_weight[i][j] < 10:
                    brick = StrongBrick(c.brick_width * j + deltax,
                                        i * c.brick_height + deltay + 80, c.brick_width,
                                        c.brick_height, StrongBrick.color)
                    bufmas.append(brick)
                    self.objects.append(brick)
                elif bricks_weight[i][j] < 30:
                    brick = MediumBrick(c.brick_width * j + deltax, i * c.brick_height + deltay + 80,
                                        c.brick_width, c.brick_height, MediumBrick.color)
                    self.objects.append(brick)
                else:
                    brick = WeakBrick(c.brick_width * j + deltax, i * c.brick_height + deltay + 80,
                                      c.brick_width, c.brick_height, WeakBrick.color)
                    bufmas.append(brick)
                    self.objects.append(brick)
                deltax += 5
            bricks.append(bufmas)
            self.bricks = bricks

    def create_score(self):
        self.score = TextObject(c.score_x, c.score_y, c.score_text, c.score_color,
                                c.score_font_filename, c.score_font_size)
        self.objects.append(self.score)

    def create_life(self, numoflife=0):
        self.life = Life(c.life_pic_filename, c.life_x[numoflife])
        self.objects.append(self.life)

    def create_objects(self):
        for i in range(3):
            self.create_life(i)
        self.create_score()
        self.create_paddle()
        self.create_ball()
        self.create_bricks()

    def ball_physics(self):
        if self.ball.centerx < self.ball.radius or c.screen_width - self.ball.centerx <= self.ball.radius:
            self.ball.dx = -self.ball.dx
            if self.ball.centerx < self.ball.radius:
                self.ball.bounds.centerx = self.ball.radius
        if self.ball.centery <= self.ball.radius:
            self.ball.dy = -self.ball.dy

    def collisioncheck(self):

        def paddleCollision(obj):
            relative_offset = self.ball.right - obj.left
            middle = obj.centerx - obj.left
            start = middle - 20
            end = obj.right - obj.left
            middle_end = middle + 20
            if relative_offset < start:
                self.ball.dx = -1 * ((start // relative_offset) % 3) if start // relative_offset < 3 else -1 * 2
            elif relative_offset > middle_end:
                self.ball.dx = 1 * relative_offset // (end - middle_end) % 3
            elif start < relative_offset < middle_end:
                self.ball.dx = -0.5 if (middle - self.ball.centerx) < 0 else 0.9

        def hit_the_brick(brick):
            brick.hits -= 1
            if brick.hits > 0:
                brick.setcolor()
            else:
                self.objects.remove(brick)
                self.points+=50
                self.setscore()

        def changeDirection(obj):
            if self.ball.dx > 0:
                offsetx = self.ball.right - obj.left
            else:
                offsetx = obj.right - self.ball.left
            if self.ball.dy > 0:
                offsety = self.ball.bottom - obj.top
            else:
                offsety = obj.bottom - self.ball.top

            if abs(offsety - offsetx) < 9:
                self.ball.dx = - self.ball.dx
                self.ball.dy = - self.ball.dy
            elif offsety > offsetx:
                self.ball.dx = - self.ball.dx
            elif offsetx > offsety:
                self.ball.dy = - self.ball.dy
        for obj in self.objects:
            if isinstance(obj, Brick):
                if pg.Rect.colliderect(self.ball.bounds, obj.bounds):
                    changeDirection(obj)
                    hit_the_brick(obj)
            elif isinstance(obj, Paddle):
                if pg.Rect.colliderect(self.ball.bounds, obj.bounds):
                    changeDirection(obj)
                    paddleCollision(obj)

    def setscore(self):
        self.score.text = f"SCORE: {self.points}"

    def setZeroPos(self):
        if self.ball.state == False:
            self.ball.bounds.centerx = self.paddle.centerx

    def update(self):
        self.ball_physics()
        self.collisioncheck()
        self.loose()
        self.setZeroPos()
        super().update()

    def loose(self):
        def countLife():
            lifeCount=0
            for i in self.objects:
                if isinstance(i, Life):
                    lifeCount += 1
                    life = i
            return lifeCount, life
        if self.ball.centery > c.screen_height:
            if countLife()[0] > 0:
                self.objects.remove(self.ball)
                self.create_ball()
                print(countLife()[1])
                todel = self.objects.index(countLife()[1])
                self.objects.remove(self.objects[todel])
            else:
                quit()



if __name__ == '__main__':
    game = Breakout(c.game_caption, c.screen_width, c.screen_height,
                    c.bg_image_filename, c.frame_rate, c.bg_music_filename)
    game.run()
