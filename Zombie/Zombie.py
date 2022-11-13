import math
from turtle import distance, pos, position
from Variables.global_variables import *
import numpy as np
import random

def length(vector):
    return np.linalg.norm(vector)

def normalize(vector):
    return np.divide(vector, length(vector))

# def get_new_orientation(self, current_orientation, velocity):
    # pass
    # if self.length(velocity) > 0:
    #     return np.arctan2(-self.static.position[0], self.static.position[1]) #??????
    # else:
    #     return current_orientation

def orientation_scalar_to_vector(vector):
    orientation_vector = [0.0, 0.0]
    orientation_vector[0] = np.sin(vector)
    orientation_vector[1] = np.cos(vector)
    return orientation_vector

def random_binomial():
    return (random.uniform(0.0, 1.0) - random.uniform(0.0, 1.0))

def map_to_range(radian):
    pom = radian%(2 * math.pi)
    pom = abs(pom)
    if pom <= math.pi:
        radian = pom
    else:
        radian = - ((2*math.pi) - pom)
    return radian

class Kinematic:
    position = [400.0, 600.0]
    orientation = 0.6
    velocity = [1.0, 0.0]
    rotation = 0.4

    def __init__(self):
        pass

    def __init__(self, position = [400.0, 600.0]):
        self.position = position

    def update(self, steering, max_speed, time):
        if steering != None:
            self.position = np.add(self.position, np.multiply(self.velocity, time))
            self.orientation = np.add(self.orientation, np.multiply(self.rotation, time))

            self.velocity = np.add(self.velocity, np.multiply(steering.linear, time))
            self.orientation = np.add(self.orientation, np.multiply(steering.angular, time))

            if length(self.velocity) > max_speed:
                self.velocity = normalize(self.velocity)
                self.velocity = np.multiply(self.velocity, max_speed)

class SteeringOutput:
    linear = [0.4, 0.0]
    angular = 0.8

    def __init__(self):
        pass

class Static:
    position = [0.0, 0.0]
    orientation = 0.0

    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

class KinematicSteeringOutput:
    velocity = [1.0, 0.0]
    rotation = 0.9

    def __init__(self):
        pass

class KinematicArrive:
    character = Static([300.0, 500.0], 0.6)
    target = Static([800.0, 500.0], 0.6)
    max_speed = 0.4
    radius = 4.0
    time_to_target = 0.25

    def __init__(self):
        pass

    def get_steering(self):
        steering = KinematicSteeringOutput()
        steering.velocity = np.subtract(self.target.position, self.character.position)
        # steering.velocity = length(steering.velocity) ?????

        if length(steering.velocity) < self.radius:
            return None

        steering.velocity = np.divide(steering.velocity, self.time_to_target)

        if length(steering.velocity) > self.max_speed:
            steering.velocity = normalize(steering.velocity)
            steering.velocity = np.multiply(steering.velocity, self.max_speed)
        
        # self.character.orientation = get_new_orientation(...)
        steering.rotation = 0.0
        return steering

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def print(self):
        print(self.character)

class KinematicWander:
    character = Static([300.0, 500.0], 0.6)
    max_speed = 3.0
    max_rotation = 10.0
    
    def __init__(self):
        pass

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def get_steering(self):
        steering = KinematicSteeringOutput()
        steering.velocity = np.multiply(self.max_speed, orientation_scalar_to_vector(self.character.orientation))
        steering.rotation = np.multiply(random_binomial(), self.max_rotation)
        return steering

class Seek:
    character = None
    target = None
    max_acceleration = 1.0 #???? array or float?

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.target.position, self.character.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.max_acceleration)
        steering.angular = 0.0
        return steering

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def __init__(self):
        self.character = Kinematic()
        self.target = Kinematic()

class Arrive:
    character = None
    # target = Kinematic()
    max_acceleration = 0.0
    max_speed = 0.0
    target_radius = 0.5
    slow_radius = 0.0
    time_to_target = 0.1

    def __init__(self):
        self.character = Kinematic()

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def get_steering(self, target):
        steering = SteeringOutput()
        direction = np.subtract(target.position, self.character.position)
        distance = length(direction)
        if distance < self.target_radius:
            return None
        if distance > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = np.divide(np.multiply(self.max_speed, distance), self.slow_radius)
        target_velocity = direction
        target_velocity = normalize(target_velocity)
        target_velocity = np.multiply(target_velocity, target_speed)

        steering.linear = np.subtract(target_velocity, self.character.velocity)
        steering.linear = np.divide(steering.linear, self.time_to_target)

        if length(steering.linear) > self.max_acceleration:
            steering.linear = normalize(steering.linear)
            steering.linear = np.multiply(steering.linear, self.max_acceleration)

        steering.angular = 0.0
        return steering


class Align:
    character = None
    target = None
    max_angular_acceleration = 10.8
    max_rotation = 900.6
    target_radius = 0.1
    slow_radius = 0.2
    time_to_target = 0.7

    def __init__(self, position = [400.0, 600.0]):
        print("ALign constructor")
        self.character = Kinematic(position)
        print("self.character = ", self.character)
        self.target = Kinematic()

    def get_character(self):
        return self.character

    def set_target_orientation(self, orientation):
        self.target.orientation = orientation

    def get_steering(self, target): #bez tego target b bierzemu z self.target???
        steering = SteeringOutput()
        rotation = np.subtract(self.target.orientation, self.character.orientation)
        rotation = map_to_range(rotation)
        rotation_size = abs(rotation)

        if rotation_size < self.target_radius:
            return None

        if rotation_size > self.slow_radius:
            target_rotation = self.max_rotation
        else:
            target_rotation = np.divide(np.multiply(self.max_rotation, rotation_size), self.slow_radius)

        target_rotation = np.multiply(target_rotation, np.divide(rotation, rotation_size))
        steering.angular = np.subtract(target_rotation, self.character.rotation)
        steering.angular = np.divide(steering.angular, self.time_to_target)

        # angular_acceleration = abs(steering.angular)
        # if angular_acceleration > self.max_angular_acceleration:
            # steering.angular = np.divide(steering.angular, angular_acceleration)
            # steering.angular = np.divide(steering.angular, self.max_angular_acceleration)

        steering.linear = 0.0
        return steering

class Face(Align):
    align = None
    target = None
    set_temporary_target = None

    def __init__(self, position = [400.0, 600.0]):
        self.align = Align(position)
        self.target = self.align.target
        self.temporary_target = Kinematic()

    def get_character(self):
        return self.align.get_character()

    def set_temporary_target(self, temporary_target):
        self.temporary_target.position = temporary_target

    def get_steering(self):
        direction = np.subtract(self.temporary_target.position, self.get_character().position)
        if length(direction) == 0.0:
            return self.target

        self.align.target = self.temporary_target #????? explicit target
        self.align.target.orientation = np.arctan2(-direction[0], direction[1])
        return self.align.get_steering(self.temporary_target)

class Wander(Face):
    wander_offset = 10.0
    wander_radius = 303.0
    wander_rate = 80.0
    wander_orientation = 3.00
    max_acceleration = 10.0
    face = None

    def __init__(self, position = [400.0, 600.0]):
        self.face = Face(position)

    def get_character(self):
        return self.face.get_character()

    # def draw_wander_circle(self):
        # position = self.face.character.position
        # pygame.draw.circle(window, (255,255,255), position, self.wander_radius)

    def get_steering(self):
        self.wander_orientation = np.add(self.wander_orientation, np.multiply(random_binomial(), self.wander_rate))
        target_orientation = np.add(self.wander_orientation, self.get_character().orientation)
        target = np.add(self.get_character().position, np.multiply(self.wander_offset, orientation_scalar_to_vector(self.get_character().orientation)))
        target = np.add(target, np.multiply(self.wander_radius, orientation_scalar_to_vector(target_orientation)))
        self.face.set_temporary_target(target)
        steering = self.face.get_steering()
        if steering == None: return None
        steering.linear = np.multiply(self.max_acceleration, orientation_scalar_to_vector(self.get_character().orientation))
        return steering

class VelocityMatch:
    character = None
    target = None
    max_acceleration = 0.0 #??? array or float???
    time_to_target = 0.1

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.target.velocity, self.character.velocity)
        steering.linear = np.divide(steering.linear, self.time_to_target)

        if length(steering.linear) > self.max_acceleration:
            steering.linear = normalize(steering.linear)
            steering.linear = np.multiply(steering.linear, self.max_acceleration)
        
        steering.angular = 0.0
        return steering

    def __init__(self):
        self.character = Kinematic()
        self.target = Kinematic()

class Pursue(Seek):
    max_prediction = 0.5
    temporary_target = None
    seek = None

    def __init__(self):
        self.temporary_target = Kinematic()
        self.seek = Seek()

    def set_temporary_target(self, temporary_target):
        self.temporary_target.position = temporary_target

    def get_steering(self):
        direction = np.subtract(self.target.position, self.character.position)
        distance = length(direction)
        speed = length(self.character.velocity)
        
        if speed <= np.divide(distance, self.max_prediction):
            prediction = self.max_prediction
        else:
            prediction = np.divide(distance, speed)

        self.seek.target = self.temporary_target
        self.seek.target.position = np.add(self.seek.target.position, np.multiply(self.target.velocity, prediction))

        return self.seek.get_steering()

class Zombie:
    color = (0, 255, 0)
    radius = 8
    time = 0.01
    wander = None

    def __init__(self, position):
        self.wander = Wander(position)

    def get_character(self):
        return self.wander.get_character()
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.get_character().position, self.radius)

    # steering behaviors: wander
    def update(self):
        self.get_character().update(self.wander.get_steering(), 10.0, self.time)