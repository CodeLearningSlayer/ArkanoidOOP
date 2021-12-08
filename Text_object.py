import pygame as pg


class TextObject:
    def __init__(self, x, y, text, color, font_path, font_size):
        self.pos = (x, y)
        self.text = text
        self.color = color
        self.font = pg.font.Font(font_path, font_size)
        self.font_size = font_size

    def draw(self, surface):
        text_surface, self.bounds = self.get_surface(self.text)
        pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(self.text, True, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass