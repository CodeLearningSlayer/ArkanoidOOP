import pygame as pg
from Game import Game
from Ball import Ball
import time
import Events as evt
from Paddle import Paddle
from Brick import StrongBrick, MediumBrick, WeakBrick, Brick
from Text_object import TextObject
import config as c
from Life import Life
from Bonus import SmallPaddle, StickyPaddle, SmallBall, Bonus
import random


class Breakout(Game):
    def __init__(self, caption, width, height, bg_img_filename, frame_rate, bg_music_filename):
        super().__init__(caption, width, height, bg_img_filename, frame_rate)
        pg.mixer.music.load(bg_music_filename)
        pg.mixer.music.play(-1, 0, 5000)
        pg.mixer.music.set_volume(0.0)
        self.gamemode = True
        self.paddle = None
        self.ball = None
        self.width = width
        self.bonuses = None
        self.height = height
        self.points = 0
        self.count_hit = 0
        self.bricks = None
        self.obj_offset = 0
        self.score = None
        self.winner_text = None
        self.lost_text = None
        self.create_handlers()
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
                    bufmas.append(brick)
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
        self.generate_bonuses()
        self.create_winner_text()
        self.create_lost_text()

    def create_winner_text(self):
        self.winner_text = TextObject(c.winner_text_x, c.winner_text_y, c.winner_text_text, c.winner_text_font_color,
                                      c.winner_text_font, c.winner_text_font_size)

    def create_lost_text(self):
        self.lost_text = TextObject(c.lost_text_x, c.lost_text_y, c.lost_text_text, c.lost_text_font_color,
                                    c.lost_text_font, c.lost_text_font_size)

    def collisioncheck(self):

        def hit_the_brick(brick):
            brick.hits -= 1
            if brick.hits > 0:
                brick.setcolor()
            else:
                self.checkBonusInside(brick)
                self.objects.remove(brick)
                self.points += 50
                self.set_score()
            brick.hit()


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
            self.ball.move(self.ball.dx, self.ball.dy)

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
            self.ball.move(self.ball.dx, self.ball.dy)

        for obj in self.objects:
            if isinstance(obj, Brick):
                if pg.Rect.colliderect(self.ball.bounds, obj.bounds):
                    changeDirection(obj)
                    hit_the_brick(obj)

            elif isinstance(obj, Paddle):
                if pg.Rect.colliderect(self.ball.bounds, obj.bounds):
                    if self.paddle.state or pg.key.get_pressed()[pg.K_SPACE]:
                        if pg.key.get_pressed()[pg.K_SPACE]:
                            self.count_hit += 1
                            if not self.check_counter(self.count_hit):
                                self.paddle.change_state()
                        changeDirection(obj)
                        paddleCollision(obj)
                    else:
                        print('yeah')
                        self.get_offset()

            elif isinstance(obj, Bonus):
                if pg.Rect.colliderect(self.paddle.bounds, obj.bounds):
                    evt.generate_bonus_action(obj)
                    self.objects.remove(obj)

    def create_smallBall(self, x, y):
        bonus = SmallBall(x, y, c.bonus_width, c.bonus_height, c.bonus_speed)
        return bonus

    def create_smallPaddle(self, x, y):
        bonus = SmallPaddle(x, y, c.bonus_width, c.bonus_height, c.bonus_speed)          # тут нужен DRY
        return bonus

    def create_stickyPaddle(self, x, y):
        bonus = StickyPaddle(x, y, c.bonus_width, c.bonus_height, c.bonus_speed)
        return bonus

    def checkBonusInside(self, brick):
        for row in self.bricks:
            if brick in row:
                i = self.bricks.index(row)
                j = row.index(brick)
                if self.bonuses[i][j]:  # сделать проверку при разбитии кирпича
                    print("тут есть бонус")
                    evt.generate_bonus_drop_event(self.bonuses[i][j])

    def BonusGeneration(self, list):
        def randomBonus(i, j):
            a = random.randint(1, 3)
            if a == 1:
                cell = self.create_smallBall(list[i][j].centerx, list[i][j].centery)
                return cell
            elif a == 2:
                cell = self.create_smallPaddle(list[i][j].centerx, list[i][j].centery)
                return cell
            else:
                cell = self.create_stickyPaddle(list[i][j].centerx, list[i][j].centery)
                return cell

        bonus_list = []
        for i in range(3):
            buflist = [None] * 12
            for j in range(c.screen_width//c.brick_width):
                if isinstance(list[i][j], StrongBrick):
                    bufrand = random.randint(1, 2)
                    if bufrand == 2:
                        buflist[j] = randomBonus(i, j)
                elif isinstance(list[i][j], MediumBrick):
                    bufrand = random.randint(1, 5)
                    if bufrand == 5:
                        buflist[j] = randomBonus(i, j)
            bonus_list.append(buflist)
        return bonus_list

    def generate_bonuses(self):
        self.bonuses = self.BonusGeneration(self.bricks)
        print(self.bonuses)

    def set_score(self):
        self.score.change_text(f"SCORE: {self.points}")

    def get_offset(self):
        if not self.paddle.state:
            self.ball.state = False
            self.obj_offset = self.ball.right-self.paddle.left

    def set_zero_pos(self):
        if not self.ball.state and not self.paddle.state:
            self.ball.set_position(self.obj_offset+self.paddle.left,
                                   self.paddle.top - self.ball.radius)
            return
        if not self.ball.state and self.paddle.state:
            self.ball.set_position(self.paddle.centerx, self.paddle.top-self.ball.radius)

    @staticmethod
    def check_counter(value):
        if value % 5 == 0:
            return False
        else:
            return True

    def handle_bonus_action(self, bonus):
        self.objects.append(bonus)

    def small_ball_action(self):
        self.ball.downscale()

    def create_handlers(self):
        self.game_events_handlers[evt.BONUS_DROP].append(self.handle_bonus_action)
        self.game_events_handlers[evt.SMALL_BALL_BONUS].append(self.small_ball_action)
        self.game_events_handlers[evt.SMALL_PADDLE_BONUS].append(self.small_paddle_action)
        self.game_events_handlers[evt.STICKY_PADDLE_BONUS].append(self.sticky_paddle_action)

    def small_paddle_action(self):
        self.paddle.downscale()

    def sticky_paddle_action(self):
        print('Работаю')
        self.paddle.change_state()

    def update(self):
        self.collisioncheck()
        self.loose()
        self.set_zero_pos()
        if self.win():
            self.win_sound()
            self.objects.remove(self.paddle)
            self.objects.remove(self.ball)
            self.message(self.winner_text)
            self.game_over = True
            time.sleep(3)
            quit()
        super().update()


    def loose(self):
        def countLife():
            lifeCount = 0
            life = 0
            for i in self.objects:
                if isinstance(i, Life):
                    lifeCount += 1
                    life = i
            return lifeCount, life
        if self.ball.centery > c.screen_height:
            if countLife()[0] > 0:
                self.objects.remove(self.ball)
                self.create_ball()
                todel = self.objects.index(countLife()[1])
                self.objects.remove(self.objects[todel])
                if not self.paddle.state:
                    self.paddle.change_state()
            else:
                self.loose_sound()
                self.objects.remove(self.paddle)
                self.objects.remove(self.ball)
                self.message(self.lost_text)
                self.game_over = True
                time.sleep(3)
                quit()   # прописать метод проигрыша

    def win(self):
        for obj in self.objects:
            if isinstance(obj, Brick):
                return False
        return True

    def message(self, obj):
        self.objects.append(obj)
        obj.draw(self.surface)
        pg.display.update()


if __name__ == '__main__':
    game = Breakout(c.game_caption, c.screen_width, c.screen_height,
                    c.bg_image_filename, c.frame_rate, c.bg_music_filename)
    game.run()
