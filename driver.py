import pygame
import math
import path_planning as pp


class Driver():
    def __init__(self, vehicle, path, settings):
        """ Driver """
        #_______main objects references_______
        #reference to driver vehicle object:
        self.vehicle = vehicle
        #creating a plan object:
        self.plan = pp.path_plan(path)


        #___________Settings_________
        #initial velocity
        self.velocity = settings._velocity_
        #allowed error range for angle
        self.angle_allowed_error = math.radians(settings._angle_allowed_error_)

        #_______Class variables_______

        #amount of degrees that it needs to turn to match desired path
        self.angle_to_turn = None
        #diretion that it needs to turn the wheel
        self.direction_to_turn = None
        #Boolean to indicate when to stop
        self.safe_to_drive = False

        self.settings = settings

    #######################################################

    def update_settings(self):
        self.angle_allowed_error = math.radians(self.settings._angle_allowed_error_)
        self.velocity = self.settings._velocity_

    def update_driving_condition(self,conditions):
        self.safe_to_drive = conditions['safe_to_drive']
        self.angle_to_turn = conditions['angle_to_turn']
        self.direction_to_turn = conditions['direction_to_turn']

    def turn_wheel(self):
        if self.angle_to_turn > self.angle_allowed_error:
            if self.direction_to_turn == 'CCW': #opposite to match screens coordinates
                self.vehicle.turn_left(self.velocity)
                return "Turning left"
            elif self.direction_to_turn == 'CW': #opposite to match screens coordinates
                self.vehicle.turn_right(self.velocity)
                return "Turning Right"
            else:
                print("I am confused!")
                return "I am confused!"
        else:
            self.vehicle.move_forward(self.velocity)
            return "Moving forward"


    def drive(self, win, draw_plan=False, draw_sensor=False, debug=False):
        self.update_settings()
        conditions = self.plan.update_plan(win,self.vehicle.position,self.vehicle.direction, draw_plan, draw_sensor, debug)
        self.update_driving_condition(conditions)
        # print(conditions)
        if self.safe_to_drive == True:
            response = self.turn_wheel()
        else:
            response = "Not safe to drive"
        return response
