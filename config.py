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
sticky_paddle_color = pg.Color('aquamarine1')

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

small_paddle_path = "sprites/SmallPaddle.jpg"
small_paddle_img = pg.image.load(small_paddle_path)
small_paddle_img = pg.transform.scale(small_paddle_img, (40,40))
small_paddle_rect = small_paddle_img.get_rect()

bonus_width = 40
bonus_height = 40
bonus_speed = 3

sourceFileDir = os.path.dirname(os.path.abspath(__file__))
path_hit = os.path.join(sourceFileDir, 'sounds/hit.wav')

winner_text_x = screen_width//2 - 300
winner_text_y = screen_height//2 - 200
winner_text_text = "YOU WIN!"
winner_text_font_size = 100
winner_text_font = score_font_filename
winner_text_font_color = (255, 215, 0)

lost_text_x = winner_text_x - 50
lost_text_y = winner_text_y
lost_text_text = "GAME OVER"
lost_text_font_color = (220, 20, 60)
lost_text_font = score_font_filename
lost_text_font_size = 100

path_win = os.path.join(sourceFileDir, 'sounds/win.mp3')
path_loose = os.path.join(sourceFileDir, 'sounds/loose.mp3')