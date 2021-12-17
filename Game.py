import random

import pygame as pg
import Events as evt
import sys
from config import path_win, path_loose
from collections import defaultdict

class Game:
    def __init__(self, caption, width, height, bg_img_filename, frame_rate):
        pg.init()
        self.bg_img = pg.image.load(bg_img_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        self.surface = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()
        self.loose_music = pg.mixer.Sound(path_loose)
        self.loose_music.set_volume(0.1)
        self.win_music = pg.mixer.Sound(path_win)
        self.win_music.set_volume(0.1)
        self.keydown_handlers = defaultdict(list)
        self.game_events_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self):
        for obj in self.objects:
            obj.draw(self.surface)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pg.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif  event.type == pg.USEREVENT+1:
                if event.MyOwnType == evt.BONUS_DROP:
                    print('бонус падает')
                    for handler in self.game_events_handlers[evt.BONUS_DROP]:
                        handler(event.value)
                if event.MyOwnType == evt.SMALL_PADDLE_BONUS:
                    for handler in self.game_events_handlers[evt.SMALL_PADDLE_BONUS]:
                        handler()
                if event.MyOwnType == evt.SMALL_BALL_BONUS:
                    for handler in self.game_events_handlers[evt.SMALL_BALL_BONUS]:
                        handler()
                if event.MyOwnType == evt.STICKY_PADDLE_BONUS:
                    for handler in self.game_events_handlers[evt.STICKY_PADDLE_BONUS]:
                        handler()

    def loose_sound(self):
        self.loose_music.play()

    def win_sound(self):
        self.win_music.play()

    def run(self):
        while not self.game_over:
            self.surface.blit(self.bg_img, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pg.display.update()
            self.clock.tick(self.frame_rate)
