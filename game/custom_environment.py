import random
import pygame as pg
from game.player import Player
from game.ball import Ball 
from game.settings import world_settings,  player_setting, ball_setting
import numpy as np
pg.init()
pg.display.set_caption("Q-Learning Pin-Pong")

class CustomEnv:
    def __init__(self):
        self.high = np.array([1.1, 1.1, 0.85,  1.03, 1.03])
        self.low = np.array([-1.1, -1.1, -0.01,  -0.04, -0.04])

        self.WIDTH = world_settings["WIDTH"]
        self.HEIGHT = world_settings["HEIGHT"]

        self.display_render = False
        self.game_over = False

        self.player = Player(self, 
            random.randint(0, self.WIDTH-player_setting["width"]),  #Randon position x 
            self.HEIGHT - player_setting["height"] - player_setting["padding"], #position bottom
        ) 
        self.autoplayer = Player(self,
            random.randint(0, self.WIDTH-player_setting["width"]), #Randon position x 
            player_setting["height"] - player_setting["padding"], #position top
        )
        self.ball = Ball(self,
            random.randint(16, self.WIDTH-16), 
            self.HEIGHT/2 - 8, 
            [self.player, self.autoplayer] #Interact with
        )
        self.clock = pg.time.Clock()
    def return_observation(self):
        return [self.ball.vector["x"], self.ball.vector["y"], self.player.x/self.WIDTH, self.ball.x/self.WIDTH, self.ball.y/self.HEIGHT]
    def reset(self):
        self.__init__()
        return self.return_observation()
    def step(self, action):
        self.ball.update() #Upgrade positon ball
        self.ball.speed += 0.001 #Acceleration
        self.player.move(action-1) #action happens input (0, 1, 2) - 1 = (-1, 0, 1)
        self.autoplayer.auto(self.ball)  #Auto move bot 
        return self.return_observation(),  self.player.score, self.game_over
    def render(self, FPS):
        if not self.display_render:
            self.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
            self.display_render = True
        pg.event.get()
        pg.display.update() 
        self.display.fill((0, 0, 0))
        self.ball.draw()
        self.player.draw()
        self.autoplayer.draw()
        self.clock.tick(FPS)