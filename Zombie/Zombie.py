from turtle import pos, position
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

class Kinematic:
    position = [400.0, 500.0]
    orientation = 0.6
    velocity = [1.0, 0.0]
    rotation = 0.4

    def __init__(self):
        pass

    def update(self, steering, time):
        self.position += np.multiply(self.velocity, time)
        self.orientation += np.multiply(self.rotation, time)

        self.velocity += np.multiply(steering.linear, time)
        self.orientation += np.multiply(steering.angular, time)

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
    max_speed = 10.0
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


class Zombie:
    color = (0, 255, 0)
    radius = 12
    time = 0.5
    kinematic = Kinematic()
    steering = SteeringOutput()
    kinematic_arrive = KinematicArrive() 
    kinematic_wander = KinematicWander()  

    def __init__(self):
        pass
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.kinematic.position, self.radius)

    # def update(self, target_center): #kinematic arrive
    #     self.kinematic_arrive.update_character(self.kinematic.position, self.kinematic.orientation)
    #     self.kinematic_arrive.target.position = target_center
    #     if self.kinematic_arrive.get_steering() != None:
    #         self.kinematic.velocity = self.kinematic_arrive.get_steering().velocity
    #         self.kinematic.rotation = self.kinematic_arrive.get_steering().rotation
    #     self.kinematic.update(self.steering, self.time)
    def update(self):
        self.kinematic_wander.update_character(self.kinematic.position, self.kinematic.orientation)
        self.kinematic.velocity = self.kinematic_wander.get_steering().velocity
        self.kinematic.rotation = self.kinematic_wander.get_steering().rotation
        self.kinematic.update(self.steering, self.time)