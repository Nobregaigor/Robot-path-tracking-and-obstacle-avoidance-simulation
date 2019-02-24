import math
import json
from pprint import pprint

class Vector():
    def __init__(self,p1,direction,magnitude):
        self.vec = {
            'i': None,
            'j': None
        }
        self.p1 = p1
        self.p2 = {
            'x': None,
            'y': None
        }
        self.direction = direction
        self.magnitude = magnitude

class CheckPoints:
    def __init__(self):
        self.indices = []
        self.vals = []

    def get_min_indice(self):
        return min(self.indices)
    def get_min_val(self):
        return min(self.vals)
    def get_max_indice(self):
        return max(self.indices)
    def get_max_val(self):
        return max(self.vals)
    def reset(self):
        self.indices = []
        self.vals = []

class Sensor:
    def __init__(self, range, angle, type, name):
        self.name = name
        self.range = range
        self.angle = angle
        self.direction = {
            'x': None,
            'y': None
        }
        self.endpoint = {
            'x': None,
            'y': None
        }
        self.status = False
        self.type = type
        self.safetry_radius = 70


        self.point_radius = 4
        self.line_color = (96, 76, 194)
        self.circle_color = (166, 110, 247)

        self.active_sensors = []

    def update_direction(self, new_dir):
        self.direction['x'] = math.cos(self.angle) * new_dir['x'] - math.sin(self.angle) * new_dir['y']
        self.direction['y'] = math.cos(self.angle) * new_dir['y'] + math.sin(self.angle) * new_dir['x']

    def update_endpoint(self, new_pos):
        self.endpoint['x']  = new_pos['x'] + (self.direction['x'] * self.range)
        self.endpoint['y']  = new_pos['y'] + (-self.direction['y'] * self.range)
