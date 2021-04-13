import os
import pygame
from math import sin, radians, degrees
from pygame.math import Vector2
from timeit import default_timer as timer
from NeuroSkyPy.NeuroSkyPy import NeuroSkyPy
import numpy as np
from time import sleep
import logging
import sys
import csv

pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

def outlineit(x, y, outline, size, string, font, color, most, screen):
    for i in string:
        if i == "m":
            font = pygame.font.Font("New Athletic M54.ttf", 30)
            x = 115
            y += 18
        if i !=" ":
            insideObj = font.render(i, 1, color)
            outsideObj = font.render(i, 1, (0, 0, 0))

            screen.blit(outsideObj, (x-outline, y-outline))
            screen.blit(outsideObj, (x-outline, y))
            screen.blit(outsideObj, (x-outline, y+outline))
            screen.blit(outsideObj, (x, y-outline))
            screen.blit(outsideObj, (x, y+outline))
            screen.blit(outsideObj, (x+outline, y-outline))
            screen.blit(outsideObj, (x+outline, y))
            screen.blit(outsideObj, (x+outline, y+outline))
            screen.blit(insideObj, (x, y))

            x+=most

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

        self.acceleration = -5.0
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

class Logger:
    def __init__(self, filename):
        self.filename = filename
        logging.basicConfig(filename=filename,
                    format='%(asctime)s,%(message)s',
                    filemode='w')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def log_message(self, message):
        self.logger.info(message)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def get_text(self):
        return(self.text)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
class Game:
    i = 0
    threshold_array = np.random.permutation([40, 50, 60])
    coins_thresh = np.array([], "int")
    trial_num = 0
    def __init__(self, subject_name):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        self.width = 800
        self.height = 447
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.exp_num = "Noisy Threshold"
        self.subject_name = subject_name
        #count files in directory
        data_folder = os.path.join(self.exp_num, self.subject_name)
        file_count = sum(len(files) for _, _, files in os.walk(data_folder))
        Game.trial_num = file_count 
        if(file_count > 0):
            Game.trial_num = Game.trial_num - 1
        # print(Game.threshold_array)

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
        global_start = timer()
        threshold = Game.threshold_array[Game.i]
        # print(threshold)

        data_folder = os.path.join(self.exp_num, self.subject_name)

        #check if data folder exists
        if not os.path.isdir(data_folder):
            os.makedirs(data_folder)

        #count files in directory
        # file_count = sum(len(files) for _, _, files in os.walk(data_folder))
        # trial_num = file_count 
        # if(file_count > 0):
        #     trial_num = trial_num - 1
        file_path = os.path.join(data_folder, "trial_{}.csv".format(Game.trial_num))

        logger = Logger(file_path)
        if(Game.i == 0):
            header = "timestamp"+","+"threshold"+","+"attention"+","+"score"+","+"spaceship_position"+","+"spaceship_velocity"
            logger.log_message(header)

        while not self.exit:
            if(timer() - global_start >= 30):
                global_start = timer()
                Game.i = Game.i + 1
                Game.coins_thresh = np.append(Game.coins_thresh, coin_list.get_score())
                if(Game.i == len(Game.threshold_array)): 
                    disp_text = self.font.render("Enter the order of difficulty/control that you experienced (Eg : 1,2,3): ", 1, (255,255,255))
                    input_box = InputBox((self.width/2), (self.height/2), 140, 32)
                    done = False
                    text = ''
                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                                text = input_box.get_text()
                                done = True
                            input_box.handle_event(event)

                        input_box.update()
                        if(done):
                            text = np.array(text.split(','), 'int')
                        self.screen.fill((30, 30, 30))
                        self.screen.blit(disp_text, ((self.width/2)-200, (self.height/2)-30))
                        input_box.draw(self.screen)
                        pygame.display.flip()

                    with open(os.path.join(data_folder, "trial_data.csv"), "a+", newline='') as f:
                        writer = csv.writer(f)
                        ground_truth = [[x] for x in Game.threshold_array]
                        for i in range(1,len(ground_truth)+1):
                            ground_truth[i-1].append(i)
                        ground_truth.sort()
                        ground_truth_trials = []
                        for i in range(len(ground_truth)):
                            ground_truth_trials.append(ground_truth[i][1])
                        if(os.stat(os.path.join(data_folder, "trial_data.csv")).st_size == 0):
                            writer.writerow(["Trial Number", "Threshold Array", "Coins Collected", "User Order", "Ground Truth"])
                        writer.writerow([Game.trial_num, Game.threshold_array, Game.coins_thresh, text, np.asarray(ground_truth_trials, 'int')])
                    print("exceeded")
                    exit()
                
                while (timer() - global_start <= 10):
                    PauseScreen = pygame.image.load("beginScreen.jpg")
                    PauseScreen = pygame.transform.scale(PauseScreen, (self.width, self.height))
                    timeRemaining = 10 - (timer() - global_start)
                    self.screen.blit(PauseScreen, (0,0))
                    outlineit(300, 200, 2, 20, "THE_GAME_RESUMES_IN", pygame.font.Font("New Athletic M54.ttf", 40), (255,140, 0), 23, self.screen)
                    outlineit(400, 300, 3, 20, str(round(timeRemaining, 3)), pygame.font.Font("New Athletic M54.ttf", 40), (255,140, 0), 23, self.screen)
                    pygame.display.flip()

                self.run(neuropy)
            attention = (neuropy.attention)
            dt = self.clock.get_time() / 100

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            car.velocity.y = ((attention - threshold) / 10)  
            # Logic
            car.update(dt)
            coin_list.update_list(car.position, car.offset)
            bg.update()

            if(car.position.y >= -5):
                car.position.y = -5
            if(car.position.y <= -self.height/ppu):
                car.position.y = -self.height/ppu

            # Logging trial data
            msg = str(threshold)+","+str(attention)+","+str(coin_list.get_score())+","+str(car.position.y)+","+str(car.velocity.y)
            logger.log_message(msg)

            # Drawing
            attention_text = self.font.render(str(txt_attention + str(attention)), 1, (255,255,255))
            score_text = self.font.render(str(txt_score + str(coin_list.get_score())), 1, (255,255,255))
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            bg.render(self.screen)
            self.screen.blit(rotated, (self.width/(0.3*ppu), -car.position.y * ppu - self.height/(0.3*ppu)))
            coin_list.render(self.screen)
            # self.screen.blit(attention_text, (self.width-190, self.height-50))
            # self.screen.blit(score_text, (self.width-190, self.height-32))
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

    #pass experiment number and subject name as command line arguments
    subject_name = sys.argv[1]

    game = Game(subject_name)
    game.run(neuropy)