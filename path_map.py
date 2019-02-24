import random
import pygame
import math

class path_map:
    def __init__(self,settings):
        #Size window for
        self.size = settings._window_size_
        #Colors of point colors
        self.pcolor = settings._points_color_
        #Radius of points
        self.pradius = settings._points_radius_
        #Color of line between points
        self.lcolor = settings._line_colors_
        #Size of line
        self.lsize = settings._line_size_
        #Number of points
        self.n_points = settings._n_points_
        #shape_mode
        self.shape_mode = 'line'

        #________points
        self.points = []
        self.pointsColor = []

        #obstacles
        self.obstacles = []
        self.obestaclesColor = (41, 111, 194)
        self.nobstacles = 4


    def createPoints(self):
        self.points = []
        n = self.n_points

        if self.shape_mode == "line":
            initialx = random.randint(30,round(self.size[0]*0.2))
            initialy = random.randint(200,400)

            self.points.append([initialx,initialy])
            self.pointsColor.append(self.pcolor)

            min = round(math.exp(-self.n_points*0.01)*15 + self.n_points*0.25)

            for i in range(n -1):
                signrand = random.choice([1,-1])

                randx = self.points[i][0] + (random.randint(min,min*2))
                randy = self.points[i][1] + (random.randint(min,min*2) * signrand)

                self.points.append([randx,randy])
                self.pointsColor.append(self.pcolor)

    def createObstacles(self):
        self.obstacles = []
        n = self.nobstacles

        initialx = random.randint(250,350)
        initialy = random.randint(300,400)
        randr = random.randint(5,100)

        obs = {
            'position': [initialx,initialy],
            'radius': randr
        }

        self.obstacles.append(obs)

        for i in range(n -1):
            signrand = random.choice([1,-1])

            randx = self.obstacles[i]['position'][0] + (random.randint(60,200))
            randy = self.obstacles[i]['position'][1] + (random.randint(50,200) * signrand)

            randr = random.randint(5,100)

            obs = {
                'position': [randx,randy],
                'radius': randr
            }

            self.obstacles.append(obs)




    def draw_circles(self,win):
        n = len(self.points)
        for i in range(n):
            pygame.draw.circle(win, self.pointsColor[i], (self.points[i][0],self.points[i][1]), self.pradius)

    def draw_lines(self,win):
        pygame.draw.lines(win, self.lcolor, False, self.points, 2)

    def draw_obstacles(self,win):
        n = len(self.obstacles)
        for i in range(n):
            pygame.draw.circle(win, self.obestaclesColor, (self.obstacles[i]['position'][0],self.obstacles[i]['position'][1]), self.obstacles[i]['radius'])


    def draw_path(self,win):
        self.draw_obstacles(win)
        self.draw_circles(win)
        self.draw_lines(win)
