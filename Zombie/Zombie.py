from turtle import position
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

class Kinematic:
    position = [400.0, 500.0]
    orientation = 0.6
    velocity = [1.0, 0.0]
    rotation = 0.4

    def __init__(self):
        pass

    # def __init__(self, position, orientation, velocity, rotation):
    #     self.position = position
    #     self.orientation = orientation
    #     self.velocity = velocity
    #     self.rotation = rotation

    def update(self, steering, time):
        self.position += np.multiply(self.velocity, time)
        self.orientation += np.multiply(self.rotation, time)

        self.velocity += np.multiply(steering.linear, time)
        self.orientation += np.multiply(steering.angular, time)

class SteeringOutput:
    linear = [0.0, 0.0]
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
    rotation = 0.4

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

class Zombie:
    color = (0, 255, 0)
    radius = 12
    time = 0.05
    kinematic = Kinematic()
    kinematic_arrive = KinematicArrive()
    # steering = SteeringOutput()

    def __init__(self):
        pass

    def draw(self):
        pygame.draw.circle(window, self.color, self.kinematic_arrive.character.position, self.radius)

    def update(self):
        self.kinematic.update(self.kinematic_arrive.get_steering(), self.time)


















# class Zombie:
#     radius = 0
#     color = (0, 255, 0)
#     # time = 0.0
#     position = [0.0, 0.0]
    # orientation = 0.0
    # velocity = [0.0, 0.0]
    # rotation = 0.0
    # steering_linear = [0.0, 0.0]
    # steering_angular = 0.0

    # # target_position = [800.0, 700.0]
    # max_speed = 10.0
    # target_radius = 0.5
    # time_to_target = 0.25

    # # #collision avoidance
    # # max_acceleration = 0.0
    # target_pos = [800.0, 700.0] #temporary

    # #wandering
    # wander_offset = 0.5
    # wander_radius = 3.0
    # wander_rate = 1.0
    # wander_orientation = [1.0, 0.0]
    # max_accelereation = 0.4 


    # def __init__(self, radius, position):
    #     self.radius = radius
    #     self.position = position
    #     # self.time = time
    #     # self.orientation = orientation
    #     # self.velocity = velocity
    #     # self.rotation = rotation
    #     # self.steering_linear = steering_linear
    #     # self.steering_angular = steering_angular

    # def draw(self):
    #     pygame.draw.circle(window, self.color, self.position, self.radius)
        
        #rysowanie celu do ktorego zmierza zombiak (tylko pomocniczo, potem wyleci)
        # pygame.draw.circle(window, (0,0,255), self.target_position, self.radius)

    # def kinematic_update(self):
    #     self.position += np.multiply(self.velocity, self.time)
    #     self.orientation += self.rotation * self.time

    #     self.velocity += np.multiply(self.steering_linear, self.time)
    #     self.orientation += self.steering_angular * self.time

    # def random_binomial(self):
    #     return random.uniform(0.0, 1.0) - random.uniform(0.0, 1.0)

    # def get_new_orientation(self):
        #TODO
        #skierowanie sie czubkiem zombiaka w kierunku celu
        #w przypadku okregu CHYBA niepotrzebne

    # def kinematic_arrive(self, target_position):
    #     self.velocity = np.subtract(target_position, self.position)
    #     if np.linalg.norm(self.velocity) < self.target_radius:
    #         return #???
    #     else:
    #         self.velocity = np.divide(self.velocity, self.time_to_target)

    #         if np.linalg.norm(self.velocity) > self.max_speed:
    #             normalized_velocity = self.velocity / np.linalg.norm(self.velocity)
    #             self.velocity = normalized_velocity
    #             self.velocity = np.multiply(self.velocity, self.max_speed)
            
    #         #face direction get_new_orientation()
    #         self.rotation = 0.0

    # def wandering(self):
    #     self.wander_orientation += np.multiply(self.random_binomial(), self.wander_rate)
    #     target_orientation = np.add(self.wander_orientation, self.orientation)
    #     self.target_pos = np.add(self.position, self.orientation)
    #     self.target_pos += np.multiply(self.wander_radius, target_orientation)

    # def collision_avoidance(self, targets):
    #     shortest_time = 99999
    #     target_velocity = [0.0, 0.0]
    #     for target in targets:
    #         relative_position = np.subtract(target.coordinates, self.position)
    #         relative_velocity = np.subtract(target_velocity, self.velocity)
    #         relative_speed = np.linalg.norm(self.velocity)
    #         time_to_collision = np.divide(np.dot(relative_position, relative_velocity), np.multiply(relative_speed, relative_speed))

    #         distance = np.linalg.norm(relative_position)
    #         min_separation = np.subtract(distance, np.multiply(relative_speed, shortest_time))
    #         if min_separation > 2*self.target_radius:
    #             print("!")
