import random
import pygame as pg
from game.settings import player_setting, ball_setting
class Ball:
    def __init__(self, this, x, y, objects=[]):
        self.this = this
        self.x = x
        self.y = y
        self.radius = ball_setting["radius"]
        self.objects = objects
        self.speed = ball_setting["speed"]
        self.vector = {
            "x": 1 if random.random()>0.5 else -1,
            "y":1 if random.random()>0.5 else -1
        }
    def update(self):
        if self.x < self.radius or self.x > self.this.WIDTH - self.radius:
            self.vector["x"] *= -1
        for obj in self.objects:
            obj.score = 0
            if self.x > obj.x and self.x < obj.x+obj.width and self.y > obj.y and self.y < obj.y+obj.height:
                self.vector["y"] *= -1

                obj.score=1
        self.x += self.vector["x"]*self.speed
        self.y += self.vector["y"]*self.speed
        if self.y < -player_setting["padding"] or  self.y-self.this.HEIGHT > 0:
            self.this.game_over =  True
    def draw(self, display = "", color = (255, 255, 255)):
        display = display if display else self.this.display
        pg.draw.circle(display, color, (self.x, self.y), self.radius)