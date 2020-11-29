import random
import pygame as pg
from game.settings import player_setting, ball_setting
class Player:
    def __init__(self, this, x, y):
        self.this = this
        self.x = x
        self.y = y
        self.width = player_setting["width"]
        self.height = player_setting["height"]
        self.speed = player_setting["speed"]
        self.score = 0
    def move(self, mx):
        mx *= self.speed
        if self.x < 0:
            mx *= 0 if mx < 0 else 1 
        if self.x > self.this.WIDTH-self.width:
            mx *= 0 if mx > 0 else 1 
        self.x +=mx
    def auto(self, to):
        c_ = self.x+self.width/2
        to_c_ = to.x + to.radius/2
        mx = to.x - c_ 
        if mx > to.speed:
            mx = 1
        elif mx < -to.speed:
            mx = -1
        else: 
            mx = 0
        self.move(mx)
    def draw(self, display = "", color = (255, 255, 255)):
        display = display if display else self.this.display
        pg.draw.rect(display, color, (self.x, self.y, self.width, self.height))