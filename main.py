import pygame
import pygame as pg
from math import *
import time
import random

gamemode = True
HEIGHT = 768
WIDTH = 1024
GAME = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
fps = 100 # изменить потом обратно
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
clock = pg.time.Clock()
sc = pg.display.set_mode((WIDTH, HEIGHT))
bg = pg.image.load("bg.jpg")
pg.font.init()
all_sprites = pg.sprite.Group()
myfont = pygame.font.SysFont('Comic Sans MS', 60)
textsurface = myfont.render('GAME OVER', False, (255, 255, 255))
active = 1
static = 0
stick = 0


class GeometryValues:

    def __set_name__(self, owner, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value


class Ball:
    dx = GeometryValues()
    dy = GeometryValues()
    radius = GeometryValues()
    def __init__(self, gamefield, color, obj):
        self.__gamefield = gamefield
        self.__color = color
        self.radius = 15
        self.__rect = int(self.radius * sqrt(2))
        self.id = pg.Rect(obj.id.centerx, obj.id.top - self.__rect - 4, self.__rect, self.__rect)
        self.__speed = 3
        self.dx = 0
        self.dy = 0
        self.__state = static
        self.__offset = 0

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    def set_offset(self, value):
        if self.__state == active:
            self.__offset = value
        elif self.__offset == 0:
            self.__offset = value

    def get_offset(self):
        return self.__offset

    def draw(self, obj):
        global GAME
        pg.draw.circle(self.__gamefield, RED, self.id.center, self.radius)
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            self.__state = active

            GAME = 1
            self.dx = 0
            self.dy = -1
        if self.id.centerx < self.radius or WIDTH - self.id.centerx <= self.radius:
            self.dx = -self.dx
        if self.id.centery <= self.radius:
            self.dy = -self.dy
        if self.__state != static or not pg.Rect.colliderect(self.id, obj.id):
            self.id.y += self.__speed * self.dy
            self.id.x += self.__speed * self.dx
            self.set_offset(0)
        else:
            self.set_offset(self.id.right - obj.id.left)
            self.drawSticky(obj)

        if GAME == 0:
            self.id.x = obj.id.centerx

    def drawSticky(self, obj):
        self.dx = 0
        self.dy = 0
        self.id.x = obj.id.x + self.get_offset()




class Paddle:
    def __init__(self, gamefield, color):
        self.__gamefield = gamefield
        self.__color = color
        self.width = 200  # setter
        self.__speed = 10
        self.__height = 25
        self.id = pg.Rect(WIDTH // 2 - self.__width // 2, HEIGHT - self.__height * 2, self.__width, self.__height) # подумать

    def draw(self):
        pg.draw.rect(self.__gamefield, pygame.Color('darkorange'), self.id)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.id.left > 0:
            self.id.left -= self.__speed
        if key[pg.K_RIGHT] and self.id.right < WIDTH:
            self.id.right += self.__speed


    def setwidth(self, width):
        self.__width = width

    width = property(fset=setwidth)

class Brick:
    Width = 80
    Height = 30

    def __init__(self, gamefield, color, x, y):
        self.__gamefield = gamefield
        self.__x = x
        self.__y = y
        self.__color = color
        self.id = pg.Rect(self.__x, self.__y, Brick.Width, Brick.Height)

    def draw(self):
        pg.draw.rect(self.__gamefield, self.__color, self.id)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class WeakBrick(Brick):
    Color = LIGHT_BLUE
    hits = 1
    pass


class MediumBrick(Brick):
    Color = GREEN
    hits = 2
    pass


class StrongBrick(Brick):
    Color = RED
    hits = 3
    pass


class UnbreakableBrick(Brick):
    pass


class Bonus:

    def __init__(self, gamefield, x, y):
        self.__gamefield = gamefield
        self.__x = x
        self.__y = y
        self.__path = (f"sprites/{self.__class__.__name__}.jpg")
        self.__image = pg.image.load(self.__path).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (40, 40))
        self.id = self.__image.get_rect()
        self.id.x = self.__x
        self.id.y = self.__y

    def draw(self):
        self.__gamefield.blit(self.__image, self.id)
        self.id.y += 1


class SmallBall(Bonus):
    @staticmethod
    def modification(obj):
        obj.id.width = 10
        obj.id.height = 10
        obj.radius = 10


class SmallPaddle(Bonus):
    @staticmethod
    def modification(obj):
        obj.id.width = 150


class StickyPaddle(Bonus):
    @staticmethod
    def modification(obj):
        obj.state = static


def collisioncheck(ball, brick):
    if ball.dx > 0:
        offsetx = ball.id.right - brick.id.left
    else:
        offsetx = brick.id.right - ball.id.left
    if ball.dy > 0:
        offsety = ball.id.bottom - brick.id.top
    else:
        offsety = brick.id.bottom - ball.id.top

    if abs(offsety - offsetx) < 9:
        ball.dx = - ball.dx
        ball.dy = - ball.dy
        print('угол')
    elif offsety > offsetx:
        ball.dx = - ball.dx
    elif offsetx > offsety:
        ball.dy = - ball.dy

    return ball.dx, ball.dy


def paddleCollision(paddle, ball):
    relative_offset = ball.id.right - paddle.id.left
    middle = paddle.id.centerx - paddle.id.left
    start = middle - 20
    end = paddle.id.right - paddle.id.left
    middle_end = middle + 20
    if relative_offset < start:
        ball.dx = -1 * ((start//relative_offset) % 3) if start//relative_offset < 3 else -1 * 2
    elif relative_offset > middle_end:
        ball.dx = 1 * relative_offset//(end - middle_end) % 3
    elif start < relative_offset < middle_end:
        ball.dx = -0.5 if (middle - ball.id.centerx) < 0 else 0.9
    return ball.dx


def BonusGeneration(list):
    bonus_list = []
    for i in range(3):
        buflist = [None] * 12
        for j in range(1024 // 80):
            if isinstance(list[i][j], StrongBrick):
                bufrand = random.randint(1, 2)
                if bufrand == 2:
                    a = random.randint(1, 3)
                    if a == 1:
                        buflist[j] = SmallBall(sc, list[i][j].id.centerx, list[i][j].id.centery)
                    elif a == 2:
                        buflist[j] = SmallPaddle(sc, list[i][j].id.centerx, list[i][j].id.centery)
                    else:
                        buflist[j] = StickyPaddle(sc, list[i][j].id.centerx, list[i][j].id.centery)
            elif isinstance(list[i][j], MediumBrick):
                bufrand = random.randint(1, 5)
                if bufrand == 5:
                    a = random.randint(1, 3)
                    if a == 1:
                        buflist[j] = SmallBall(sc, list[i][j].id.centerx, list[i][j].id.centery)
                    elif a == 2:
                        buflist[j] = SmallPaddle(sc, list[i][j].id.centerx, list[i][j].id.centery)
                    else:
                        buflist[j] = StickyPaddle(sc, list[i][j].id.centerx, list[i][j].id.centery)
        bonus_list.append(buflist)
    return bonus_list


def TypeOfBonus(obj):
    if isinstance(obj, SmallBall) or isinstance(obj, StickyPaddle) :
        return "Ball"
    else:
        return "Paddle"



paddle = Paddle(sc, PINK)
ball = Ball(sc, RED, paddle)
rand__ranges = [10, 30, 60]
bricks_weight = [[random.randint(0, 100) for j in range(WIDTH // Brick.Width)] for i in range(3)]
bricks = []
bufrand = 0
deltay = 0
for i in range(3):
    bufmas = []
    deltax = 10
    deltay += 2
    for j in range(1024 // 80):
        if bricks_weight[i][j] < 10:
            bufmas.append(StrongBrick(sc, StrongBrick.Color, Brick.Width * j + deltax, i * Brick.Height + deltay))
        elif bricks_weight[i][j] < 30:
            bufmas.append(MediumBrick(sc, MediumBrick.Color, Brick.Width * j + deltax, i * Brick.Height + deltay))
        else:
            bufmas.append(WeakBrick(sc, WeakBrick.Color, Brick.Width * j + deltax, i * Brick.Height + deltay))
        deltax += 5
    bricks.append(bufmas)
bonus = BonusGeneration(bricks)
bonusfall = 0
bonus_sprites = []
print(bonus)
pg.display.flip()
while gamemode:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamemode = False
    sc.blit(bg, (0, 0))
    for i in range(3):
        for j in range(1024 // 80):
            if isinstance(bricks[i][j], Brick):
                bricks[i][j].draw()
                if pg.Rect.colliderect(ball.id, bricks[i][
                    j].id):  # Первый вариант проверки удара, минус в том, что наезжает мячик. Аналог - по координатам проверка.
                    ball.dx, ball.dy = collisioncheck(ball, bricks[i][j])
                    fps += 2
                    if bricks[i][j].hits == 3:

                        bricks[i][j].color = GREEN
                        bricks[i][j].hits -= 1
                    elif bricks[i][j].hits == 2:

                        bricks[i][j].color = LIGHT_BLUE
                        bricks[i][j].hits -= 1
                    else:
                        if bonus[i][j]:
                            bonus_sprites.append(bonus[i][j])
                        bricks[i][j] = 0
    # print(bonus_sprites)
    if len(bonus_sprites) != 0:
        for i in range(len(bonus_sprites)):
            print(bonus_sprites)
            if bonus_sprites[i]:
                bonus_sprites[i].draw()
            if bonus_sprites[i].id.y >= HEIGHT:
                bonus_sprites.pop(i)
                break
            if pg.Rect.colliderect(bonus_sprites[i].id, paddle.id):  # придумать тут таймер для бонусов
                if TypeOfBonus(bonus_sprites[i]) == "Ball":
                    print("ball was given")
                    bonus_sprites[i].modification(ball)
                    bonus_sprites.pop(i)
                    break
                else:
                    print("paddle was given")
                    bonus_sprites[i].modification(paddle)
                    bonus_sprites.pop(i)
                    break

    if HEIGHT - ball.id.centery > ball.radius:
        ball.draw(paddle)
    paddle.draw()
    if pg.Rect.colliderect(ball.id, paddle.id):
        ball.dx, ball.dy = collisioncheck(ball, paddle)
        ball.dx = paddleCollision(paddle, ball)
    if HEIGHT - ball.id.centery <= ball.radius:
        sc.blit(textsurface, (WIDTH // 2, HEIGHT // 2))
        pg.display.flip()
        time.sleep(1)
        quit()
    pg.display.flip()
    clock.tick(fps)