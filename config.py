#main configuration set up

###################################
###     Model Car Settings      ###
###################################

class Car_Settings:
    def __init__(self):
        #Initial position
        self._initial_position_ = {'x': 50, 'y': 50}
        #Initial angle
        self._initial_angle_ = 0
        #Velocity
        self._veloticy_ = 10 #px/click
        #Angle resolution
        self._angle_resolution_ = 10 #degre/click
        #size
        self._size_ = 10 #px
        #color
        self._color_ = (255, 0, 0)
        #initial unit vector


###################################
###      Path map Settings      ###
###################################

class Path_Map_Settings:
    def __init__(self):
        #Size window for
        self._window_size_ = [1200,800]
        #Colors of point colors
        self._points_color_ = (43, 220, 235)
        #Radius of points
        self._points_radius_ = 7
        #Color of line between points
        self._line_colors_ = (35, 123, 187)
        #Size of line
        self._line_size_ = 6
        #number of points
        self._n_points_ = 35


###################################
###   Path Planning Settings    ###
###################################
class Path_Planning_Settings:
    def __init__(self):
        #Outer range radius
        self._outer_range_radius_ = 200
        #outer range color
        self._outer_range_color_ = (23, 228, 40)
        #Inner range radius
        self._inner_range_radius_ = 20
        #Inner range color
        self._inner_range_color_ = (23, 228, 40)
        #Desired path color
        self._desired_path_color_ = (255, 255, 255)
        #Desired path resolution (interpolation between points)
        self._desired_path_resolution_ = 50

###################################
###  Autonomous Driver Settings ###
###################################
class Autonomous_Driver_Settings:
    def __init__(self):
        #allowed error range for angle
        self._angle_allowed_error_ = 10 #deg
        self._velocity_ = 5



###################################
###    Home Screen Settings     ###
###################################
