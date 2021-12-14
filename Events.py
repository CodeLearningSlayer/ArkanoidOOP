import pygame as pg
from Bonus import SmallPaddle, SmallBall, StickyPaddle
BONUS_DROP = 0
SMALL_PADDLE_BONUS = 1
SMALL_BALL_BONUS = 2
STICKY_PADDLE_BONUS = 3


def generate_bonus_drop_event(bonus):
    bonus_drop_event = pg.event.Event(pg.USEREVENT+1, MyOwnType=BONUS_DROP, value=bonus)
    pg.event.post(bonus_drop_event)


def generate_bonus_action(bonus):
    if isinstance(bonus, SmallPaddle):
        small_paddle_event = pg.event.Event(pg.USEREVENT+1, MyOwnType=SMALL_PADDLE_BONUS)
        pg.event.post(small_paddle_event)
    if isinstance(bonus, SmallBall):
        small_ball_event = pg.event.Event(pg.USEREVENT+1, MyOwnType=SMALL_BALL_BONUS)
        pg.event.post(small_ball_event)
    if isinstance(bonus, StickyPaddle):
        sticky_paddle_event = pg.event.Event(pg.USEREVENT+1, MyOwnType=STICKY_PADDLE_BONUS)
        pg.event.post(sticky_paddle_event)

