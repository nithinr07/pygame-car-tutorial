import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from timeit import default_timer as timer
from NeuroSkyPy.NeuroSkyPy import NeuroSkyPy
from time import sleep
import random
import tkinter as tk
from tkinter import ttk
from numpy import random

class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('stars.png')
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width

            self.moving_speed = 2
          
      def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
             
      def render(self, DISPLAYSURF):
         DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
         DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))
class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=1000.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 2000
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.offset = (6 * 25) + (5 * 20)

        self.acceleration = -6.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (0, self.acceleration * dt)
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

class Coin:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.collision = False
        self.coin_img = pygame.image.load("coin.png")
        self.coin_img = pygame.transform.scale(self.coin_img, (25, 25))
        self.moving_speed = 2

    def update(self, car_position, offset):
        self.position.x -= self.moving_speed
        if(car_position.x + offset >= self.position.x and car_position.x + offset <= self.position.x + 25 and car_position.y >= self.position.y and car_position.y <= self.position.y + 25):
            self.collision = True
    
    def render(self, DISPLAYSURF):
        if(self.collision == False):
            DISPLAYSURF.blit(self.coin_img, self.position)

class CoinList:
    def __init__(self, num_coins=2000):
        self.num_coins = num_coins
        self.coins = []
        self.offset = 800
        self.score = 0

    def get_position(self):
        return(self.coins[25].position)
    
    def get_score(self):
        return(self.score)

    def create_list(self):
        for i in range(self.num_coins):
             self.coins.append(Coin(self.offset + (i * 20), -5))
     
    def update_list(self, car_position, offset):
        self.score = 0
        for coin in self.coins:
            coin.update(car_position, offset)
            if(coin.collision == True):
                self.score += 1
    
    def render(self, DISPLAYSURF):
        for coin in self.coins:
            coin.render(DISPLAYSURF)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.width = 800
        self.height = 447
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self, neuropy):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        car_image_path = os.path.join(current_dir, "spaceship.png")
        car_image = pygame.image.load(car_image_path)
        bg = Background()
        car_image = pygame.transform.scale(car_image, (100,75))
        ppu = 16
        # Edges are (0,0); (self.width/ppu, 0); (0, self.height/ppu); (self.width/ppu, self.height/ppu)
        car = Car(self.width/(2*ppu), self.height/(2*ppu))
        coin_list = CoinList()
        coin_list.create_list()
        txt_attention = "Attention: "
        txt_velocity = "Velocity: "
        txt_score = "Score: "
        threshold = random.normal(loc=0, scale=5)
        while not self.exit:
            attention = (neuropy.attention)
            dt = self.clock.get_time() / 100

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            car.velocity.y = ((attention - 50) / 10) + threshold  
            # Logic
            car.update(dt)
            coin_list.update_list(car.position, car.offset)
            bg.update()

            if(car.position.y >= -5):
                car.position.y = -5
            if(car.position.y <= -self.height/ppu):
                car.position.y = -self.height/ppu

            # Drawing
            attention_text = self.font.render(str(txt_attention + str(attention)), 1, (255,255,255))
            score_text = self.font.render(str(txt_score + str(coin_list.get_score())), 1, (255,255,255))
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            bg.render(self.screen)
            self.screen.blit(rotated, (self.width/(0.3*ppu), -car.position.y * ppu - self.height/(0.3*ppu)))
            coin_list.render(self.screen)
            self.screen.blit(attention_text, (self.width-190, self.height-50))
            self.screen.blit(score_text, (self.width-190, self.height-32))
            pygame.display.flip()
            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    os.system("sudo rfcomm connect /dev/rfcomm0 C4:64:E3:E6:E3:7D 1 &")
    sleep(5)
    neuropy = NeuroSkyPy("/dev/rfcomm0")
    neuropy.start()
    print("Initialising....")
    sleep(5)
    while(neuropy.poorSignal != 0):
        print("Wear Headset Properly:", neuropy.poorSignal)
    game = Game()
    game.run(neuropy)