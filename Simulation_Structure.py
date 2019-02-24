import pygame
from globals import *

import pygame
import car
import path_map as pm
import driver as dr
import config
import math
import random

import os


x = 50
y = 80
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


pygame.init()

class simulationStructure():
    def __init__(self,pygame):

        self.window = pygame.display.set_mode((win_width,win_height))
        pygame.display.set_caption('Project Demeter')
        self.clock = pygame.time.Clock()

        self.home_background_image = pygame.image.load(home_background_image).convert()

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def display_text(self, msg, font, color, x_displace=0, y_displace=0, center=True, size="small"):
        textSurf, textRect = self.text_objects(msg, font, color)
        if center == True:
            textRect.center = (win_width / 2)+x_displace, (win_height / 2)+y_displace
        else:
            textRect.center = x_displace, y_displace
        self.window.blit(textSurf, textRect)


    def game_intro(self):

        intro = True
        pygame.mixer.music.load(theme_song)
        pygame.mixer.music.play(-1)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    if event.key == pygame.K_q:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        quit()
                    # if event.key == pygame.K_o:
                    #     intro = False
                    #     self.game_options()
                    if event.key == pygame.K_s:
                        intro = False
                        pygame.mixer.music.stop()
                        self.simulation_loop()
                    if event.key == pygame.K_f:
                        intro = False
                        pygame.mixer.music.stop()
                        self.fun_loop()



            self.window.blit(self.home_background_image, [0, 0])
            self.display_text("Project", sub_header, white,-75,-60)
            self.display_text("Demeter", header, green_theme)
            self.display_text("Simulation (S)", options_font, white, 0, 150)
            self.display_text("Fun Mode (F)", options_font, white, 0, 190)
            # self.display_text("Options (O)", options_font, white, 0, 230)
            self.display_text("Quit (Q)", options_font, white, 0, 230)




            pygame.display.update()
            self.clock.tick(15)

    def game_options(self):

        options_screen = True

        while options_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_b:
                        intro = False
                        self.game_intro()


            self.window.blit(self.home_background_image, [0, 0])
            self.display_text("Project", sub_header, white,-75,-60)
            self.display_text("Option 1 (1)", options_font, white, 0, 150)
            self.display_text("Demeter", header, green_theme)
            self.display_text("Option 2 (2)", options_font, white, 0, 190)
            self.display_text("Option 3 (3)", options_font, white, 0, 230)
            self.display_text("Back (B)", options_font, white, 0, 270)




            pygame.display.update()
            self.clock.tick(15)


    def simulation_loop(self):

        #___________Model Car
        Car_Settings = config.Car_Settings()
        demeter = car.AwesomeCar(Car_Settings)
        #initial Position
        vel = 10

        #___________Path_map
        path_map_settings = config.Path_Map_Settings()
        path_points = pm.path_map(path_map_settings)
        path_points.createPoints()
        path_points.createObstacles()

        #__________Autonomous driver
        drive_settings = config.Autonomous_Driver_Settings()
        driver = dr.Driver(demeter, path_points, drive_settings)

        #___________Path_plan
        driver.plan.initialize(self.window,demeter.position,demeter.direction)

        #Deviating sensors
        driver.plan.create_sensor(100, 0,   'd', 'd_f')
        driver.plan.create_sensor(80, 25,  'd','d_dl')
        driver.plan.create_sensor(80, -25, 'd','d_dr')
        driver.plan.create_sensor(60, 55,  'd','d_dl')
        driver.plan.create_sensor(60, -55, 'd','d_dr')
        #Safety sensors
        driver.plan.create_sensor(30, 0,   's','s_f')
        driver.plan.create_sensor(30, 30,  's','s_dl')
        driver.plan.create_sensor(30, -30, 's','s_dr')
        driver.plan.create_sensor(30, 90,  's','s_sr')
        driver.plan.create_sensor(30, -90, 's','s_sl')
        # #back sensors
        driver.plan.create_sensor(60, 180, 's','s_b')


        run = True
        driving_conditions = None


        start_time = pygame.time.get_ticks()
        draw_sensors = False
        draw_plan = False

        while run:
            pygame.time.delay(60) #Hz

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
            if keys[pygame.K_m]:
                pygame.mixer.music.stop()
                run = False
                self.game_intro()
            if keys[pygame.K_a]:
                drive_settings._velocity_ += 1
            if keys[pygame.K_d]:
                drive_settings._velocity_ -= 1
            if keys[pygame.K_w]:
                drive_settings._angle_allowed_error_ += 1
            if keys[pygame.K_s]:
                drive_settings._angle_allowed_error_ -= 1
            if keys[pygame.K_LEFT]:
                demeter.position['x'] -= 10
            if keys[pygame.K_RIGHT]:
                demeter.position['x'] += 10
            if keys[pygame.K_UP]:
                demeter.position['y'] -= 10
            if keys[pygame.K_DOWN]:
                demeter.position['y'] += 10
            if keys[pygame.K_1]:
                if draw_sensors == False:
                    draw_sensors = True
                else:
                    draw_sensors = False
            if keys[pygame.K_2]:
                if draw_plan == False:
                    draw_plan = True
                else:
                    draw_plan = False
            if keys[pygame.K_r]:
                path_points.createPoints()
                driver.plan.reset_checkpoints()
                demeter.position['x'] = 50
                demeter.position['y'] = 50
                start_time = pygame.time.get_ticks()
                path_points.createObstacles()


            #___________________ Main simulation Loop _____________________#

            self.window.blit(self.home_background_image, [0, 0])
            path_points.draw_path(self.window)
            demeter.draw_car(self.window)

            print(str(draw_plan))

            response = driver.drive(self.window, draw_plan, draw_sensors)


            rel_time = round((pygame.time.get_ticks() - start_time)/1000,4)


            #Display options
            # self.display_text("Use arrows to create disturbance", simulation_text, white, (win_width -150), (30), False)
            # self.display_text("Increase velocity (A)", simulation_text, white, (win_width -100), (50), False)
            # self.display_text("Decrease velocity (D)", simulation_text, white, (win_width -100), (70), False)
            # self.display_text("Increase A. error (W)", simulation_text, white, (win_width -100), (90), False)
            # self.display_text("Decrease A. error (S)", simulation_text, white, (win_width -100), (110), False)
            # self.display_text("Restart Path points (R)", simulation_text, white, (win_width -110), (130), False)
            #
            # self.display_text("Menu (M)", simulation_text, white, (win_width -50), (win_height -40), False)
            # self.display_text("Quit (Q)", simulation_text, white, (win_width -50), (win_height -20), False)
            #
            # #Display outputs
            # self.display_text("Time running [sec]: ", simulation_text, white, 110, (win_height -120),False)
            # self.display_text(str(rel_time), simulation_text, white, 230, (win_height -120),False)
            # self.display_text("Current speed [px/sec] ", simulation_text, white, 125, (win_height -100),False)
            # self.display_text(str(drive_settings._velocity_), simulation_text, white, 235, (win_height -100),False)
            # self.display_text("Allowed angle error: ", simulation_text, white, 115, (win_height -80),False)
            # self.display_text(str(drive_settings._angle_allowed_error_), simulation_text, white, 230, (win_height -80),False)
            # att = round(math.degrees(driving_conditions['angle_to_turn']),4)
            # self.display_text("Angles to turn: ", simulation_text, white, 90, (win_height -60),False)
            # self.display_text(str(att), simulation_text, white, 230, (win_height -60),False)
            # self.display_text("Direction to turn: ", simulation_text, white, 100, (win_height-40),False)
            # self.display_text(driving_conditions['direction_to_turn'], simulation_text, white, 220, (win_height-40),False)
            # self.display_text("Driver response: ", simulation_text, white, 100, (win_height-20),False)
            # self.display_text(response, simulation_text, white, 250, (win_height-20),False)

            pygame.display.update()

        pygame.quit()


    def fun_loop(self):
        #___________Model Car
        Car_Settings = config.Car_Settings()
        demeter = car.AwesomeCar(Car_Settings)
        #initial Position
        vel = 10

        #___________Path_map
        path_map_settings = config.Path_Map_Settings()
        path_points = pm.path_map(path_map_settings)
        path_points.createPoints()
        path_points.createObstacles()

        #__________Autonomous driver
        drive_settings = config.Autonomous_Driver_Settings()
        driver = dr.Driver(demeter, path_points, drive_settings)

        #___________Path_plan
        driver.plan.initialize(self.window,demeter.position,demeter.direction)

        run = True
        driving_conditions = None

        pygame.mixer.music.load(fun_song)
        pygame.mixer.music.play(-1)

        start_time = pygame.time.get_ticks()

        while run:
            pygame.time.delay(60) #Hz

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
            if keys[pygame.K_m]:
                pygame.mixer.music.stop()
                run = False
                self.game_intro()
            if keys[pygame.K_LEFT]:
                demeter.turn_left(drive_settings._velocity_)
            if keys[pygame.K_RIGHT]:
                demeter.turn_right(drive_settings._velocity_)
            if keys[pygame.K_UP]:
                demeter.move_forward(drive_settings._velocity_)
            if keys[pygame.K_DOWN]:
                demeter.move_backward(drive_settings._velocity_)
            if keys[pygame.K_a]:
                drive_settings._velocity_ += 1
            if keys[pygame.K_d]:
                drive_settings._velocity_ -= 1
            if keys[pygame.K_a]:
                drive_settings._velocity_ += 1
            if keys[pygame.K_d]:
                drive_settings._velocity_ -= 1
            if keys[pygame.K_r]:
                path_points.createPoints()
                driver.plan.reset_checkpoints()
                demeter.position['x'] = 50
                demeter.position['y'] = 50
                start_time = pygame.time.get_ticks()
                path_points.createObstacles()


            #___________________ Main simulation Loop _____________________#

            self.window.blit(self.home_background_image, [0, 0])
            path_points.draw_path(self.window)
            demeter.draw_car(self.window)

            driver.plan.update_plan(self.window,demeter.position,demeter.direction, draw_plan=True, debug=False)
            rel_time = round((pygame.time.get_ticks() - start_time)/1000,4)


            # #Display options
            # self.display_text("Use arrows to create disturbance", simulation_text, white, (win_width -150), (30), False)
            # self.display_text("Increase velocity (A)", simulation_text, white, (win_width -100), (50), False)
            # self.display_text("Decrease velocity (D)", simulation_text, white, (win_width -100), (70), False)
            # self.display_text("Restart Path points (R)", simulation_text, white, (win_width -110), (90), False)
            #
            # self.display_text("Menu (M)", simulation_text, white, (win_width -50), (win_height -40), False)
            # self.display_text("Quit (Q)", simulation_text, white, (win_width -50), (win_height -20), False)
            #
            # #Display outputs
            # self.display_text("Time running [sec]: ", simulation_text, white, 110, (win_height -100),False)
            # self.display_text(str(rel_time), simulation_text, white, 230, (win_height -100),False)
            # self.display_text("Current speed [px/sec] ", simulation_text, white, 125, (win_height -80),False)
            # self.display_text(str(drive_settings._velocity_), simulation_text, white, 235, (win_height -80),False)
            # att = round(math.degrees(driving_conditions['angle_to_turn']),4)
            # self.display_text("Angles to turn: ", simulation_text, white, 90, (win_height -60),False)
            # self.display_text(str(att), simulation_text, white, 230, (win_height -60),False)
            # self.display_text("Direction to turn: ", simulation_text, white, 100, (win_height-40),False)
            # self.display_text(driving_conditions['direction_to_turn'], simulation_text, white, 220, (win_height-40),False)

            pygame.display.update()

        pygame.quit()



test = simulationStructure(pygame)
test.game_intro()
