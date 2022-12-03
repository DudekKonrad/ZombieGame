import math

import pygame.draw

from Variables.global_variables import *
from Variables.zombie_variables import *
import numpy as np
import random


def length(vector):
    return np.linalg.norm(vector)


def normalize(vector):
    return np.divide(vector, length(vector))


def orientation_scalar_to_vector(vector):
    orientation_vector = [0.0, 0.0]
    orientation_vector[0] = np.sin(vector)
    orientation_vector[1] = np.cos(vector)
    return orientation_vector


def random_binomial():
    return random.uniform(0.0, 1.0) - random.uniform(0.0, 1.0)


def map_to_range(radian):
    pom = radian % (2 * math.pi)
    pom = abs(pom)
    if pom <= math.pi:
        radian = pom
    else:
        radian = - ((2 * math.pi) - pom)
    return radian


class Static:
    position = [0.0, 0.0]
    orientation = 0.0

    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation


def getNewOrientation(orientation, velocity):
    if length(velocity) > 0:
        return math.atan2(-velocity[0], velocity[1])
    else:
        return orientation


class Kinematic:
    position = [1.0, 1.0]
    orientation = 0.0
    velocity = [1.0, 0.0]
    rotation = 0.0
    angle = 0

    def __init__(self, position):
        self.position = position
        pass

    def update(self, steering, max_speed, my_time):
        if steering is not None:
            self.position = np.add(self.position, np.multiply(self.velocity, my_time))
            self.orientation = np.add(self.orientation, np.multiply(self.rotation, my_time))

            self.velocity = np.add(self.velocity, np.multiply(steering.linear, my_time))
            # self.orientation = getNewOrientation(self.orientation, self.velocity)
            self.rotation = np.add(self.rotation, np.multiply(steering.angular, my_time))

            if length(self.velocity) > max_speed:
                self.velocity = normalize(self.velocity)
                self.velocity = np.multiply(self.velocity, max_speed)

        # Drawing velocity vector
        pygame.draw.line(window, (0, 0, 255), self.position, self.position + self.velocity * 15, 2)
        # Drawing orientation
        vec = pygame.math.Vector2(0, 100).rotate(self.angle)
        pt_x, pt_y = self.position[0] + vec.x, self.position[1] + vec.y
        new_o = getNewOrientation(self.rotation, self.velocity)
        self.angle = math.degrees(new_o)
        pygame.draw.line(window, (110, 10, 155), self.position, (pt_x, pt_y), 2)


class SteeringOutput:
    linear = [0, 0]
    angular = 0

    def __init__(self):
        pass


class Seek:
    character = None
    target = None

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.target.position, self.character.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.character.max_acceleration)
        self.character.orientation = getNewOrientation(self.character.orientation, steering.linear)
        steering.angular = 0.0
        return steering


class Flee:
    character = None
    target = None

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.character.position, self.target.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.character.max_acceleration)
        steering.angular = 0.0
        return steering


class Arrive:
    character = None
    target = None
    target_radius = 10
    slow_radius = 0.0
    time_to_target = 0.1

    def __init__(self, character, target):
        self.character = character
        self.target = target

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
            target_speed = self.character.max_speed
        else:
            target_speed = np.divide(np.multiply(self.character.max_speed, distance), self.slow_radius)
        target_velocity = direction
        target_velocity = normalize(target_velocity)
        target_velocity = np.multiply(target_velocity, target_speed)

        steering.linear = np.subtract(target_velocity, self.character.velocity)
        steering.linear = np.divide(steering.linear, self.time_to_target)

        if length(steering.linear) > self.character.max_acceleration:
            steering.linear = normalize(steering.linear)
            steering.linear = np.multiply(steering.linear, self.character.max_acceleration)

        steering.angular = 0.0
        return steering


class Wander:
    character = None
    target = None
    circle_pos = [0, 0]
    wander_ring_distance = 2

    def __init__(self, character):
        self.character = character

    def get_steering(self):
        self.circle_pos = self.get_circle_pos()
        target_pos = self.circle_pos + pygame.math.Vector2(self.wander_ring_distance, 0).rotate(random.uniform(0, 360))
        self.target = Static(target_pos, 0)
        seek = Seek(self.character, self.target)
        return seek.get_steering()

    def get_circle_pos(self):
        x = np.add(self.character.position, np.multiply(normalize(self.character.velocity), self.wander_ring_distance))
        return x


class Zombie(Kinematic):
    steering = None
    target = None
    max_acceleration = 10
    radius = ZOMBIE_RADIUS

    def set_target(self, target_position):
        self.target = Static(target_position, 0)

    def set_kinematic_target(self, target):
        self.target = target

    def set_steering(self, option):
        if option == "Seek":
            self.steering = Seek(self, self.target)
        elif option == "Flee":
            self.steering = Flee(self, self.target)
        elif option == "Arrive":
            self.steering = Arrive(self, self.target)
        elif option == "Wander":
            self.steering = Wander(self)
        # elif option == "Align":
        #     self.steering = Align(self, self.target)
        # elif option == "VelocityMatch":
        #     self.steering = VelocityMatch(self, self.target)

    def run(self):
        self.update(self.steering.get_steering(), ZOMBIE_MAX_SPEED, ZOMBIE_TIME)
        self.draw()

    def draw(self):
        pygame.draw.circle(window, ZOMBIE_COLOR, self.position, ZOMBIE_RADIUS)
