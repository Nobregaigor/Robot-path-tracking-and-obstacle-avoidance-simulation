import pygame
import math
from config import Car_Settings

class AwesomeCar():
    def __init__(self,settings):
        #initial position
        self.position = settings._initial_position_
        #Initial angle
        self.angle = settings._initial_angle_
        #Velocity
        self.vel = settings._veloticy_
        #Angle resolution
        self.angle_resolution = settings._angle_resolution_
        #size
        self.size = settings._size_
        #color
        self.color = settings._color_

        self.direction = {
        'x': 1,
        'y': 0
        }

        # self.direction = pygame.Vector2(1, 0)

    ############################################################



    def turn_left(self,val):
        self.position['x'] += round((val/2)*self.direction['x'])
        self.position['y'] += round((val/2)*-self.direction['y'])
        self.rotate('cw') #flipped to show on screen
        self.update_direction()
        # if self.angle != math.radians(180):
        #     if self.direction['y'] > 0:
        #         self.rotate('cw')
        #     else:
        #         self.rotate('ccw')
        #     self.update_direction()
    def turn_right(self,val):
        self.position['x'] += round((val/2)*self.direction['x'])
        self.position['y'] += round((val/2)*-self.direction['y'])
        self.rotate('ccw') #flipped to show on screen
        self.update_direction()
        # if self.angle != math.radians(0):
        #     if self.direction['y'] > 0:
        #         self.rotate('ccw')
        #     else:
        #         self.rotate('cw')
        #     self.update_direction()
    def move_forward(self,val):
        self.position['x'] += round(val*self.direction['x'])
        self.position['y'] += round(val*-self.direction['y'])
        # if self.angle != math.radians(90):
        #     if self.direction['x'] > 0:
        #         self.rotate('cw')
        #     else:
        #         self.rotate('ccw')
        #     self.update_direction()
    def move_backward(self,val):
        self.position['x'] += round(val*self.direction['x'])*-1
        self.position['y'] += round(val*-self.direction['y'])*-1
        # if self.angle != math.radians(270):
        #     if self.direction['x'] > 0:
        #         self.rotate('ccw')
        #     else:
        #         self.rotate('cw')
        #     self.update_direction()

    def rotate(self,dir):
        if dir == "cw":
            self.angle += round(math.radians(self.angle_resolution),1)
        elif dir =="ccw":
            self.angle -= round(math.radians(self.angle_resolution),1)

        if self.angle >= math.radians(360):
            self.angle -= math.radians(360)
        if self.angle <= math.radians(0):
            self.angle += math.radians(360)

        a_err = 4
        if math.radians(0+a_err) >= self.angle <= math.radians(360-a_err):
            self.angle = math.radians(0)
        if math.radians(90-a_err) <= self.angle <= math.radians(90+a_err):
            self.angle = math.radians(90)
        if math.radians(180-a_err) <= self.angle <= math.radians(180+a_err):
            self.angle = math.radians(180)
        if math.radians(270-a_err) <= self.angle <= math.radians(270+a_err):
            self.angle = math.radians(270)

    def update_direction(self):
        self.direction['x'] = math.cos(self.angle)
        self.direction['y'] = math.sin(self.angle)

    def draw_car(self,win):
        pygame.draw.circle(win, self.color, (self.position['x'], self.position['y']), self.size)
        xu = self.position['x']+(20*self.direction['x'])
        yu = self.position['y']+(-20*self.direction['y'])
        pygame.draw.line(win, (224, 219, 101), (self.position['x'], self.position['y']), (xu, yu), 5)
