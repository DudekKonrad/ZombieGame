import math
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


class Kinematic:
    position = [1.0, 1.0]
    orientation = 0.0
    velocity = [1.0, 0.0]
    rotation = 0.0

    def __init__(self, position):
        self.position = position
        pass

    def update(self, steering, max_speed, my_time):
        if steering is not None:
            self.position = np.add(self.position, np.multiply(self.velocity, my_time))
            self.orientation = np.add(self.orientation, np.multiply(self.rotation, my_time))

            self.velocity = np.add(self.velocity, np.multiply(steering.linear, my_time))
            self.orientation = np.add(self.orientation, np.multiply(steering.angular, my_time))

            if length(self.velocity) > max_speed:
                self.velocity = normalize(self.velocity)
                self.velocity = np.multiply(self.velocity, max_speed)


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


class Align:
    pass


class Face(Align):
    pass


class Wander(Face):
    pass


class Pursue(Seek):
    max_prediction = 0.5

    def get_steering(self):
        direction = np.subtract(self.target.position, self.character.position)
        distance = length(direction)
        speed = length(self.character.velocity)

        if speed <= np.divide(distance, self.max_prediction):
            prediction = self.max_prediction
        else:
            prediction = np.divide(distance, speed)

        self.target.position = np.add(self.target.position, np.multiply(self.target.velocity, prediction))

        return self.get_steering()


class Zombie(Kinematic):
    steering = None
    target = None
    max_acceleration = 10

    def set_target(self, target_position):
        self.target = Static(target_position, 0)

    def set_steering(self, option):
        if option == "Seek":
            self.steering = Seek(self, self.target)
        elif option == "Flee":
            self.steering = Flee(self, self.target)
        elif option == "Arrive":
            self.steering = Arrive(self, self.target)

    def run(self):
        self.update(self.steering.get_steering(), ZOMBIE_MAX_SPEED, ZOMBIE_TIME)
        self.draw()

    def draw(self):
        pygame.draw.circle(window, ZOMBIE_COLOR, self.position, ZOMBIE_RADIUS)
        pygame.draw.circle(window, (0, 0, 255), self.position, 4)
