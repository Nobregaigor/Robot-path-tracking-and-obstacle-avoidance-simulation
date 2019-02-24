import pygame
import math
import numpy as np
from scipy import interpolate
from scipy.interpolate import interp1d
import catmull_rom_curve as catmull
from config import Path_Planning_Settings as settings
from objects import *

class path_plan():
    def __init__(self,path_map):
        #Outer range radius
        self.outer_range_radius = settings()._outer_range_radius_
        #outer range color
        self.outer_range_radius_color = settings()._outer_range_color_
        #Inner range radius
        self.inner_range_radius =  settings()._inner_range_radius_
        #Inner range color
        self.inner_range_color = settings()._inner_range_color_

        #Desired path resolution (interpolation between points)
        self.path_resolution = settings()._desired_path_resolution_

        self.path_map = path_map

        #________ Position
        self.position = {'x': None, 'y': None}
        self.direction = {'x': None, 'y': None}

        #_________ Checkpoints
        #object that holds all points that are inside the range
        self.cp_in_range = CheckPoints()
        #object that holds all points that were checked
        self.cp_done = CheckPoints()
        # self.cp_done.indices.append[-1]
        #object that holds all points that are unable to reach
        self.cp_inaccessible = CheckPoints()

        self.next_cp = None
        self.last_cp = None

        #_________ Path
        self.desired_path = []
        #Desired path color
        self.path_color = settings()._desired_path_color_

        #________ angle
        #Angle difference between the car direction and the desired path
        self.angle_error = None
        self.angle_direction = None

        #_________ Safety
        self.safe_to_drive = False

        #_________ Sensors
        self.sensors = []
        self.active_sensors = []


    ######################################################

    #___________ Update values _______________#
    def update_Position(self,new_P):
        self.position = new_P

    def update_Direction(self,new_dir):
        self.direction = new_dir

    def update_nextPoint(self):
        #when the robot is out of range, it will need to know which point it should go to
        if len(self.cp_done.indices) >= 1:
            self.next_cp = self.cp_done.get_max_indice() + 1
        else:
            self.next_cp = 0

    def update_lastPoint(self):
        self.last_cp = len(self.path_map.points)

    def reset_checkpoints(self):
        self.cp_done.reset()
        self.cp_inaccessible.reset()
        self.cp_in_range.reset()


    def create_sensor(self, range, angle, type, name):
        angle = math.radians(angle)
        #creating and updating sensor values sensor
        sensor = Sensor(range, angle, type, name)
        sensor.update_direction(self.direction)
        sensor.update_endpoint(self.position)

        self.sensors.append(sensor)

    def update_sensors(self):
        n = len(self.sensors)
        for i in range(n):
            self.sensors[i].update_direction(self.direction)
            self.sensors[i].update_endpoint(self.position)


    #___________ Sensing the enviromet  _______________#
    def check_cp_in_range(self):
        n = len(self.path_map.points)
        xc = self.position['x']
        yc = self.position['y']
        self.cp_in_range.reset()

        for i in range(n):
            xp = self.path_map.points[i][0]
            yp = self.path_map.points[i][1]

            d = math.sqrt( (xp - xc)**2 + (yp - yc)**2 )

            if i not in self.cp_done.indices:
                if (d <= self.outer_range_radius) and (d > self.inner_range_radius):
                    self.path_map.pointsColor[i] = (255, 180, 0)
                    self.cp_in_range.indices.append(i)
                    self.cp_in_range.vals.append(self.path_map.points[i])
                elif (d <= self.inner_range_radius):
                    self.path_map.pointsColor[i] = (108, 242, 30)
                    self.cp_done.indices.append(i)
                    self.cp_done.vals.append(self.path_map.points[i])
                else:
                    self.path_map.pointsColor[i] = self.path_map.pcolor


    def check_sensors(self):
        n = len(self.sensors)
        n2 = len(self.path_map.obstacles)

        self.active_sensors = []
        for i in range(n):
            xc = self.sensors[i].endpoint['x']
            yc = self.sensors[i].endpoint['y']
            for j in range(n2):

                xp = self.path_map.obstacles[j]['position'][0]
                yp = self.path_map.obstacles[j]['position'][1]

                d = math.sqrt( (xp - xc)**2 + (yp - yc)**2 )
                err = self.path_map.obstacles[j]['radius']

                if (d <= err):
                    self.active_sensors.append(i)
                else:
                    pass

    def filter_cp_in_range(self):
        n = len(self.sensors)

        for i in range(n):
            if i in self.active_sensors:
                if self.sensors[i].name in ['d_dr', 'd_dl']:
                    xc = self.sensors[i].endpoint['x']
                    yc = self.sensors[i].endpoint['y']

                    n2 = len(self.cp_in_range.indices)
                    # print(str(self.cp_in_range.indices))
                    for j in range(n2):
                        # print(j)
                        xp = self.cp_in_range.vals[j][0]
                        yp = self.cp_in_range.vals[j][1]

                        d = math.sqrt( (xp - xc)**2 + (yp - yc)**2 )
                        if (d < self.sensors[i].safetry_radius):
                            if self.cp_in_range.indices[j] not in self.cp_inaccessible.indices:
                                self.cp_inaccessible.indices.append(self.cp_in_range.indices[j])
                            self.path_map.pointsColor[self.cp_in_range.indices[j]] = (255, 0, 0)


    #___________ Calculating desired path _______________#

    def get_desired_path(self):
        #function to calculate "best path"

        #storing x's and y's separately for future function
        xs = [self.position['x']]
        ys = [self.position['y']]
        #emptying array to store path values
        self.desired_path = []
        #checking the length of points in range
        n = len(self.cp_in_range.indices)
        #if it is not the last point, calculate best trajectory line
        if (self.next_cp != self.last_cp):
            #if it has a near point and is not the first point
            if (n > 1) and (self.next_cp > 0):
                #appending x's and y's in xs and ys to use in next function
                for i in range(n):
                    # print('points in rang = ' + str(self.cp_in_range.indices))
                    # print('close points   = ' + str(self.close_points))
                    #check if point is not acsessible
                    if self.cp_in_range.indices[i] not in self.cp_inaccessible.indices:
                        xs.append(self.cp_in_range.vals[i][0])
                        ys.append(self.cp_in_range.vals[i][1])

                #if there is enough points, get a better estimation (catmull requires min of 3 points)
                if len(xs) >  2:
                    #catmull (modified cubic spline)
                    #getting interpolated points
                    cat_points = catmull.catmull_rom(xs,ys,50)
                    #resetting the path coordinates array
                    path_coords = [[xs[0],ys[0]]]
                    #checking how many points cat_points returned
                    n = len(cat_points[0])
                    for i in range(n):
                        #appending path coordinates in [x,y] format
                        path_coords.append([cat_points[0][i],cat_points[1][i]])
                    #storing desired path
                    self.desired_path = path_coords
                else:
                    xs.append(self.path_map.points[self.next_cp][0])
                    ys.append(self.path_map.points[self.next_cp][1])
                    self.desired_path.append([xs[0],ys[0]])
                    self.desired_path.append([xs[1],ys[1]])

            else:
                xs.append(self.path_map.points[self.next_cp][0])
                ys.append(self.path_map.points[self.next_cp][1])
                self.desired_path.append([xs[0],ys[0]])
                self.desired_path.append([xs[1],ys[1]])

        else:
            print('REACHED ALL POINTS')


    #___________ Calculating angle to turn _______________#

    def get_angle_error(self):
        #-- calculating the angle between vectors --
        #getting point based on unit vector (direction) and current position
        xu = self.position['x']+(1*self.direction['x'])
        yu = self.position['y']+(-1*self.direction['y']) #*-1 to match coordinates of the screen
        #creating a line for vector calculation
        line1 = [(self.position['x'],self.position['y']),(xu,yu)]
        #calculating vector 1
        vec1 = [line1[1][0]-line1[0][0],line1[1][1]-line1[0][1]]
        vec2 = [0,0]
        count = 0
        #checking if vec2 is 0 (same point)
        while (vec2[0] == 0) and (vec2[1] == 0):
            line2 = [(self.desired_path[0][0],self.desired_path[0][1]),(self.desired_path[count][0],self.desired_path[count][1])]
            vec2 = [line2[1][0]-line2[0][0],line2[1][1]-line2[0][1]]
            count += 1
        #getting vector magnitude
        mv1 = math.sqrt((vec1[0])**2 + (vec1[1])**2)
        mv2 = math.sqrt((vec2[0])**2 + (vec2[1])**2)
        #calculating angle between the vectors
        theta = math.acos((vec1[0]*vec2[0] + vec1[1]*vec2[1])/(abs(mv1)*abs(mv2)))
        #storing angle
        self.angle_error = theta
        #-- calculating which direction the car should turn
        #calculating delta between vectors: δ=u1v2−u2v1
        delta = vec1[0]*vec2[1] - vec1[1]*vec2[0]
        #checking conditions
        if delta > 0:
            self.angle_direction = 'CW'
        else:
            self.angle_direction = 'CCW'

    #Overwriting
    def react_based_on_sensor(self):
        n = len(self.active_sensors)
        for i in range(n):
            sensor = self.sensors[self.active_sensors[i]]

            if sensor.name == 'd_f':
                print("Reduce speed")
            if sensor.name == 'd_dr':

                self.angle_direction = 'CCW'
                self.angle_error = 1.57079632679
                # self.cp_in_range.indices.insert(1,0)
                # self.cp_in_range.vals.insert(1,[round(sensor.endpoint['x']),round(sensor.endpoint['y'])])
            if sensor.name == 'd_dl':
                self.angle_direction = 'CW'
                self.angle_error = 1.57079632679
                # self.cp_in_range.indices.insert(1,0)
                # self.cp_in_range.vals.insert(1,[round(sensor.endpoint['x']),round(sensor.endpoint['y'])])
            # if sensor.name in ['s_sr', 's_sl']:
            #     print("Something on the sides! be carefull")
            #     # self.safe_to_drive = False
            # if sensor.name in ['s_f', 's_dr', 's_dl']:
            #     print("Something right ahead, STOP!")
            #     self.safe_to_drive = False
            # else:
            #     self.safe_to_drive = True






    #___________ Drawing functions _______________#
    # def set_cp_inaccessible_color(self):
    #     n = len(self.cp_inaccessible.indices)
    #     for i in range(n):
    #         # print(str(i))
    #         if i in self.cp_done.indices:
    #             pass
    #         else:
    #             self.path_map.pointsColor[i] = (255, 0, 7)



    def draw_desired_path(self,win):
        if len(self.desired_path) > 1:
            pygame.draw.lines(win, self.path_color, False, self.desired_path, 4)

    def draw_range_radius(self,win):
        pygame.draw.circle(win, self.outer_range_radius_color, (self.position['x'],self.position['y']), self.outer_range_radius, 2)
        pygame.draw.circle(win, self.outer_range_radius_color, (self.position['x'],self.position['y']), self.inner_range_radius, 2)

    def draw_sensors(self,win):
        n = len(self.sensors)
        for i in range(n):
            sensor = self.sensors[i]
            pygame.draw.line(win, sensor.line_color, (self.position['x'], self.position['y']), (sensor.endpoint['x'],sensor.endpoint['y']), 2)
            if i not in self.active_sensors:
                pygame.draw.circle(win, sensor.circle_color, (round(sensor.endpoint['x']),round(sensor.endpoint['y'])), sensor.point_radius)
            else:
                pygame.draw.circle(win, (255, 0, 0), (round(sensor.endpoint['x']),round(sensor.endpoint['y'])), sensor.point_radius)
            if self.sensors[i].name in ['d_dr', 'd_dl']:
                pygame.draw.circle(win, sensor.circle_color, (round(sensor.endpoint['x']),round(sensor.endpoint['y'])), sensor.safetry_radius,2)

    def draw_plan(self,win):
        # self.set_cp_inaccessible_color()
        self.draw_desired_path(win)
        self.draw_range_radius(win)

    def initialize(self,win, newposition, newdirection,):
        self.update_Position(newposition)
        self.update_Direction(newdirection)
        self.update_nextPoint()
        self.update_lastPoint()
        if len(self.sensors) > 1:
            self.update_sensors(win)

    def update_plan(self, win, newposition, newdirection, draw_plan=False, draw_sensors=False, debug=False):
        self.update_Position(newposition)
        self.update_Direction(newdirection)
        self.update_nextPoint()
        self.update_lastPoint()

        if (self.next_cp != self.last_cp):
            self.check_cp_in_range()

            if len(self.sensors) >= 1:
                self.update_sensors()
                self.check_sensors()
                self.filter_cp_in_range()
                # self.set_cp_inaccessible_color()

            self.get_desired_path()
            self.get_angle_error()
            if len(self.active_sensors) >= 1:
                self.react_based_on_sensor()
            else:
                self.safe_to_drive = True

        else:
            self.safe_to_drive = False

        if draw_plan == True:
            self.draw_plan(win)
        if draw_sensors == True:
            self.draw_sensors(win)

        if debug == True:
            print("-----------")
            print("In range points = " + str(self.cp_in_range.indices))
            print("Done points     = " + str(self.cp_done.indices))
            print("Next point = " + str(self.next_cp))
            print("angle between vectors = " + str(math.degrees(self.angle_error)))
            print("angle direction = " + str(self.angle_direction))


        return {'angle_to_turn': self.angle_error, 'direction_to_turn': self.angle_direction, 'safe_to_drive': self.safe_to_drive}
