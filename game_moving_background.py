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
          
      def update(self, moving_speed):
        self.bgX1 -= moving_speed
        self.bgX2 -= moving_speed
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

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        # self.velocity += (self.acceleration * dt, 0)
        # self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


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

    def popupmsg(self, msg):
        while(neuropy.poorSignal != 0):
            popup = tk.Tk()
            popup.wm_title("!")
            label = ttk.Label(popup, text=msg)
            label.pack(side="top", fill="x", pady=10)
            if(neuropy.poorSignal == 0) :
                popup.destroy
                break
            # B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
            # B1.pack()
            # popup.mainloop()

    def run(self, neuropy):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "spaceship.png")
        # background_path = os.path.join(current_dir, "stars.png")
        car_image = pygame.image.load(image_path)
        bg = Background()
        # scale = Vector2(car_image.getwidth()/self.width, car_image.get_height()/self.height)
        car_image = pygame.transform.scale(car_image, (100,75))
        # background = pygame.image.load(background_path).convert()
        ppu = 16
        # Edges are (0,0); (self.width/ppu, 0); (0, self.height/ppu); (self.width/ppu, self.height/ppu)
        # car = Car(0, self.height/(2*ppu))
        car = Car(0, 0)
        prev_time = 0;
        txt = "End to End Time: "
        txt_attention = "Attention:   "
        txt_acceleration = "Acceleration: "
        start = timer()
        while not self.exit:
            self.popupmsg("Wear headset properly")
            attention = (neuropy.attention)
            # attention = random.random() * (100)
            # print(attention)
            dt = self.clock.get_time() / 100

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            # pressed = pygame.key.get_pressed()
            # car.acceleration = ((attention - 50) / 10 )
            car.velocity.x = (attention - 50) / 10  
            # + random.normal(loc=0, scale=5)
            # print(car.acceleration)
            print(car.velocity.x)
            # Logic
            car.update(dt)
            bg.update(car.velocity.x)
            # print(start-timer())
            
            # if(prev_time == 0):
            #     counting_string = txt + "nil" 
            # else:
            #     counting_string = txt + str(prev_time)
            # if(car.position.x >= self.width/ppu):
            #     end = timer()
            #     time_seconds = end - start
            #     prev_time = time_seconds
            #     counting_string = txt + str(time_seconds)
            #     car.position.x = 0
            #     # car.position.y = self.height/(2*ppu)
            #     car.position.y = 0
            #     car.velocity.x = 0
            #     start = timer()
            # if(car.position.x <= 0):
            #     car.position.x = 0
            #     if(car.velocity.x <= 0):
            #         car.velocity.x = 0

            # Drawing
            # counting_text = self.font.render(str(counting_string), 1, (255,255,255))
            attention_text = self.font.render(str(txt_attention + str(attention)), 1, (255,255,255))
            # acceleration_text = self.font.render(str(txt_acceleration + str(car.acceleration)), 1, (255,255,255))
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            # self.screen.blit(background, -car.position * ppu - (rect.width / 2, rect.height / 2))
            bg.render(self.screen)
            self.screen.blit(rotated, (self.width/(0.3*ppu), self.height/(0.3*ppu)))
            self.screen.blit(attention_text, (self.width-190, 2))
            # self.screen.blit(acceleration_text, (self.width-190, 20))
            # self.screen.blit(counting_text, (2, 2))
            
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