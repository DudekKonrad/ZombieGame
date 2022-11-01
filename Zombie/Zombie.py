from math import dist
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

    def update(self, steering, max_speed, time):
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

class Seek:
    character = Static([300.0, 500.0], 0.6)
    target = Static([800.0, 500.0], 0.6)
    max_acceleration = 0.0 #???? array or float?

    def get_steering(self):
        steering = SteeringOutput()
        print(self.target.position)
        steering.linear = np.subtract(self.target.position, self.character.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.max_acceleration)
        steering.angular = 0.0
        return steering

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def __init__(self):
        pass

class Arrive:
    character = Kinematic() #TU MA BYC KINEAMTIC DATA!!!!!!!!
    target = Kinematic()
    max_acceleration = 0.0
    max_speed = 0.0
    target_radius = 0.5
    slow_radius = 0.0
    time_to_target = 0.1

    def __init__(self):
        pass

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def get_steering(self):
        steering = SteeringOutput()
        direction = np.subtract(self.target.position, self.character.position)
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


class Zombie:
    color = (0, 255, 0)
    radius = 12
    time = 0.5
    kinematic = Kinematic()
    steering = SteeringOutput()
    kinematic_arrive = KinematicArrive() 
    kinematic_wander = KinematicWander()
    seek = Seek()
    arrive = Arrive()

    def __init__(self):
        pass
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.arrive.character.position, self.radius)

    # def update(self, target_center): #kinematic arrive
    #     self.kinematic_arrive.update_character(self.kinematic.position, self.kinematic.orientation)
    #     self.kinematic_arrive.target.position = target_center
    #     if self.kinematic_arrive.get_steering() != None:
    #         self.kinematic.velocity = self.kinematic_arrive.get_steering().velocity
    #         self.kinematic.rotation = self.kinematic_arrive.get_steering().rotation
    #     self.kinematic.update(self.steering, self.time)
    
    # def update(self): #kinematic wander
    #     self.kinematic_wander.update_character(self.kinematic.position, self.kinematic.orientation)
    #     self.kinematic.velocity = self.kinematic_wander.get_steering().velocity
    #     self.kinematic.rotation = self.kinematic_wander.get_steering().rotation
    #     self.kinematic.update(self.steering, self.time)

    # #steering behaviors: seek
    # def update(self, target_center):
    #     self.seek.update_character(self.kinematic.position, self.kinematic.orientation)
    #     self.seek.target.position = target_center
    #     self.steering.angular = self.seek.get_steering().angular
    #     self.steering.linear = self.seek.get_steering().linear
    #     self.kinematic.update(self.steering, 0.1, self.time)

    #steering behaviors: arrive
    def update(self, target_center):
        # self.arrive.update_character(self.kinematic.position, self.kinematic.orientation)
        self.arrive.target.position = target_center
        # if self.arrive.get_steering() != None:
            # self.kinematic.velocity = self.kinematic_arrive.get_steering().velocity
            # self.kinematic.rotation = self.kinematic_arrive.get_steering().rotation
        self.arrive.character.update(self.arrive.get_steering(), 0.1, self.time)