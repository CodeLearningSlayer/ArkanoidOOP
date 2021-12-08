import pygame as pg
import os
from math import *

RED = (255, 0, 0)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)

screen_width = 1024
screen_height = 768
frame_rate = 90
game_caption = "Арканоид"
bg_image_filename = ('bg.jpg')
bg_music_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music/music2.mp3')

paddle_width = 200
paddle_height = 25
paddle_color = pg.Color('darkorange')
paddle_speed = 10

ball_radius = 13
ball_side = int(ball_radius * sqrt(2))
ball_color = pg.Color('red1')
ball_speed = 3
ball_dx = 0
ball_dy = 0

score_font_filename = ('fonts/2015 Cruiser Bold.otf')
score_font_size = 50
score_x = 10
score_y = 8
score_color = (124, 252, 0)
score_text = 'score: '

brick_width = 80
brick_height = 30
brick_color = (255, 255, 255)

life_pic_filename = ('sprites/life.png')
life_x=[870, 920, 970]