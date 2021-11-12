import pygame
import os
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
fps = 100  # изменить потом обратно
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
clock = pg.time.Clock()
sc = pg.display.set_mode((WIDTH, HEIGHT))
bg = pg.image.load("bg.jpg")
pg.init()
all_sprites = pg.sprite.Group()
myfont = pygame.font.SysFont('Comic Sans MS', 60)
textsurface = myfont.render('GAME OVER', False, (255, 255, 255))
score_font = pygame.font.Font('2015 Cruiser Bold.otf', 50)
gamescore = 0
active = 1
static = 0
stick = 0

musicpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music/music2.mp3')
pg.mixer.music.load(musicpath)
pg.mixer.music.play()
pg.mixer.music.set_volume(0.1)

class GetId:

    def __set_name__(self, owner, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class Ball:
    # dx = GeometryValues()
    # dy = GeometryValues()
    # radius = GeometryValues()
    def __init__(self, gamefield, color, obj):
        self.__gamefield = gamefield
        self.__color = color
        self.radius = 13
        self.__rect = int(self.radius * sqrt(2))
        self.__id = pg.Rect(obj.id.centerx, obj.id.top - self.__rect - 4, self.__rect, self.__rect)
        self.__speed = 3
        self.__dx = 0
        self.__dy = 0
        self.__state = static
        self.__offset = 0
        self.__hit = ''

    def state(self, state):
        self.__state = state

    def set_offset(self, value):
        if self.__state == active:
            self.__offset = value
        elif self.__offset == 0:
            self.__offset = value

    def hit(self):
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(sourceFileDir, 'sounds/hit.wav')
        self.__hit = pg.mixer.Sound(path)
        self.__hit.set_volume(0.1)
        self.__hit.play()

    def get_offset(self):
        return self.__offset

    def draw(self, obj):
        global GAME
        pg.draw.circle(self.__gamefield, RED, self.__id.center, self.radius)
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.__state == static:
            self.__state = active
            GAME = 1
            self.__dx = 0
            self.__dy = -1
        if self.__id.centerx < self.radius or WIDTH - self.__id.centerx <= self.radius:
            self.__dx = -self.__dx
            if self.__id.centerx < self.radius:
                self.__id.centerx = self.radius
        if self.__id.centery <= self.radius:
            self.__dy = -self.__dy
        if self.__state != static or not pg.Rect.colliderect(self.__id, obj.id):
            self.__id.y += self.__speed * self.__dy
            self.__id.x += self.__speed * self.__dx
            self.set_offset(0)
        else:
            self.set_offset(self.__id.right - obj.id.left)
            self.__drawSticky(obj)

        if GAME == 0:
            self.__id.x = obj.id.centerx

    def __drawSticky(self, obj):
        self.__dx = 0
        self.__dy = 0
        self.__id.x = obj.id.x + self.get_offset()

    def collisioncheck(self, brick):
        if self.__dx > 0:
            offsetx = self.__id.right - brick.id.left
        else:
            offsetx = brick.id.right - self.__id.left
        if self.__dy > 0:
            offsety = self.__id.bottom - brick.id.top
        else:
            offsety = brick.id.bottom - self.__id.top

        if abs(offsety - offsetx) < 9:
            self.__dx = - self.__dx
            self.__dy = - self.__dy
            print('угол')
        elif offsety > offsetx:
            self.__dx = - self.__dx
        elif offsetx > offsety:
            self.__dy = - self.__dy

    def paddleCollision(self, paddle):
        relative_offset = self.__id.right - paddle.id.left
        middle = paddle.id.centerx - paddle.id.left
        start = middle - 20
        end = paddle.id.right - paddle.id.left
        middle_end = middle + 20
        if relative_offset < start:
            self.__dx = -1 * ((start // relative_offset) % 3) if start // relative_offset < 3 else -1 * 2
        elif relative_offset > middle_end:
            self.__dx = 1 * relative_offset // (end - middle_end) % 3
        elif start < relative_offset < middle_end:
            self.__dx = -0.5 if (middle - self.__id.centerx) < 0 else 0.9

    @property
    def id(self):
        return self.__id

class Paddle:
    def __init__(self, gamefield, color):
        self.__gamefield = gamefield
        self.__color = color
        self.width = 200  # setter
        self.__speed = 10
        self.__height = 25
        self.__id = pg.Rect(WIDTH // 2 - self.__width // 2, HEIGHT - self.__height * 2, self.__width, self.__height) # подумать

    def draw(self):
        pg.draw.rect(self.__gamefield, pygame.Color('darkorange'), self.__id)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.__id.left > 0:
            self.__id.left -= self.__speed
        if key[pg.K_RIGHT] and self.__id.right < WIDTH:
            self.__id.right += self.__speed

    @property
    def id(self):
        return self.__id

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
        self.__id = pg.Rect(self.__x, self.__y, Brick.Width, Brick.Height)

    def draw(self):
        pg.draw.rect(self.__gamefield, self.__color, self.__id)

    @property
    def id(self):
        return self.__id

    def setcolor(self):
        if self.hits == 1:
            self.__color = LIGHT_BLUE
        elif self.hits == 2:
            self.__color = GREEN
        elif self.hits == 3:
            self.__color = RED


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


class Life:
    def __init__(self, gamefield):
        self.__path = ('sprites/life.png')
        self.__image = pg.image.load(self.__path).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (50, 50))
        self.__id = self.__image.get_rect()
        self.__gamefield = gamefield
    def draw(self, coordx):
        self.__gamefield.blit(self.__image, (coordx + 870, 15))

    @property
    def id(self):
        return self.__id

class Bonus:

    def __init__(self, gamefield, x, y):
        self.__gamefield = gamefield
        self.__x = x
        self.__y = y
        self.__path = (f"sprites/{self.__class__.__name__}.jpg")
        self.__image = pg.image.load(self.__path).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (40, 40))
        self.__id = self.__image.get_rect()
        self.__id.x = self.__x
        self.__id.y = self.__y

    def draw(self):
        self.__gamefield.blit(self.__image, self.__id)
        self.__id.y += 1

    @property
    def id(self):
        return self.__id

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
        obj.state(static)


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
            bufmas.append(StrongBrick(sc, StrongBrick.Color, Brick.Width * j + deltax , i * Brick.Height + deltay + 80))
        elif bricks_weight[i][j] < 30:
            bufmas.append(MediumBrick(sc, MediumBrick.Color, Brick.Width * j + deltax , i * Brick.Height + deltay + 80))
        else:
            bufmas.append(WeakBrick(sc, WeakBrick.Color, Brick.Width * j + deltax, i * Brick.Height + deltay + 80))
        deltax += 5
    bricks.append(bufmas)
bonus = BonusGeneration(bricks)
bonusfall = 0
print(bonus)
bonus_sprites = []
pg.display.flip()
life = [Life(sc) for i in range(3)]
while gamemode:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamemode = False
    sc.blit(bg, (0, 0))
    score = score_font.render(f'SCORE: {gamescore}', True, (124,252,0))
    for i in range(3):
        for j in range(1024 // 80):
            if len(life) > 0:
                life[j % len(life)].draw(life[j % len(life)].id.width * (j%len(life)))
            if isinstance(bricks[i][j], Brick):
                bricks[i][j].draw()
                bricks[i][j].setcolor()
                if pg.Rect.colliderect(ball.id, bricks[i][j].id):
                    ball.collisioncheck(bricks[i][j])
                    ball.hit()
                    fps += 2
                    if bricks[i][j].hits == 3:
                        bricks[i][j].hits -= 1
                        bricks[i][j].setcolor()
                    elif bricks[i][j].hits == 2:
                        bricks[i][j].hits -= 1
                        bricks[i][j].setcolor()
                    else:
                        if bonus[i][j]:
                            bonus_sprites.append(bonus[i][j])
                        bricks[i][j] = 0
                        gamescore += 50
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
    sc.blit(score, (10, 8))
    if pg.Rect.colliderect(ball.id, paddle.id):
        ball.collisioncheck(paddle)
        ball.paddleCollision(paddle)
    if HEIGHT - ball.id.centery <= ball.radius:
        life.pop()
        del ball
        fps = 100
        if len(life) > 0:
            ball = Ball(sc, RED, paddle)
            GAME = 0
        else:
            sc.blit(textsurface, ((WIDTH // 2) - 150, HEIGHT // 2))
            pg.display.flip()
            time.sleep(1)
            quit()
    pg.display.flip()
    clock.tick(fps)
