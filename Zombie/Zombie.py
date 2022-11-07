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
    position = [400.0, 500.0]
    orientation = 0.6
    velocity = [1.0, 0.0]
    rotation = 0.4

    def __init__(self):
        pass

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
    character = Kinematic()
    target = Kinematic()
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
        pass

class Arrive:
    character = Kinematic() #TU MA BYC KINEAMTIC DATA!!!!!!!!
    # target = Kinematic()
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
    character = Kinematic()
    target = Kinematic()
    max_angular_acceleration = 0.8
    max_rotation = 0.6
    target_radius = 0.1
    slow_radius = 0.2
    time_to_target = 0.7

    def __init__(self):
        pass

    def set_target_orientation(self, orientation):
        self.target.orientation = orientation

    def get_steering(self, target): #bez tego target b bierzemu z self.target???
        # print("target = ", target)
        steering = SteeringOutput()
        rotation = np.subtract(self.target.orientation, self.character.orientation)
        # print("self.target.orientation = ", self.target.orientation)
        # print("self.character.orientation = ", self.character.orientation)
        # print("rotation = ", rotation)
        rotation = map_to_range(rotation)
        # print("after mapTORange rotation = ", rotation)
        rotation_size = abs(rotation)
        # print("rotation size = ", rotation_size)

        if rotation_size < self.target_radius:
            # print("if rotation_size < self.target_radius")
            return None

        if rotation_size > self.slow_radius:
            # print("if rotation_size > self.slow_radius:")
            target_rotation = self.max_rotation
            # print("target_rotation = ", target_rotation)
        else:
            # print("else")
            # print("self.maxRotation = ", self.max_rotation)
            # print("rotationsize = ", rotation_size)
            # print("self.slowradius = ", self.slow_radius)
            target_rotation = np.divide(np.multiply(self.max_rotation, rotation_size), self.slow_radius)

        # print("targetrotation = ", target_rotation)
        # print("rotation = ", rotation)
        # print("rotationsize = ", rotation_size)
        # print("np.divide(rotation, rotation_size) = ", np.divide(rotation, rotation_size))
        target_rotation = np.multiply(target_rotation, np.divide(rotation, rotation_size))
        # print("targetrotation = ", target_rotation)
        # print("self.characterrotation = ", self.character.rotation)
        steering.angular = np.subtract(target_rotation, self.character.rotation)
        # print("steering.angular = ", steering.angular)
        steering.angular = np.divide(steering.angular, self.time_to_target)

        # angular_acceleration = abs(steering.angular)
        # if angular_acceleration > self.max_angular_acceleration:
            # steering.angular = np.divide(steering.angular, angular_acceleration)
            # steering.angular = np.divide(steering.angular, self.max_angular_acceleration)

        steering.linear = 0.0
        return steering

class Face(Align):
    align = Align()
    target = align.target
    temporary_target = Kinematic()

    def __init__(self):
        pass

    def set_temporary_target(self, temporary_target):
        self.temporary_target.position = temporary_target

    def get_steering(self):
        # print("self.temporary_target.position = ", self.temporary_target.position)
        # print("self.character.position = ", self.character.position)
        direction = np.subtract(self.temporary_target.position, self.character.position)
        # print("direction = ", direction)
        if length(direction) == 0.0:
            return self.target

        self.align.target = self.temporary_target #????? explicit target
        # print("self.align.target = ", self.align.target)
        # print("direction[0] = ", direction[0])
        # print("direction[1] = ", direction[1])
        self.align.target.orientation = np.arctan2(-direction[0], direction[1])
        # print("self.align.target.orientation = ", self.align.target.orientation)
        return self.align.get_steering(self.temporary_target)

class Wander(Face):
    wander_offset = 10.0
    wander_radius = 10.0
    wander_rate = 10.0
    wander_orientation = 10.00
    max_acceleration = 10.0
    face = Face()

    def __init__(self):
        pass

    # def draw_wander_circle(self):
        # position = self.face.character.position
        # pygame.draw.circle(window, (255,255,255), position, self.wander_radius)

    def get_steering(self):
        # print("xd")
        self.wander_orientation = np.add(self.wander_orientation, np.multiply(random_binomial(), self.wander_rate))
        target_orientation = np.add(self.wander_orientation, self.character.orientation)
        target = np.add(self.character.position, np.multiply(self.wander_offset, orientation_scalar_to_vector(self.character.orientation)))
        target = np.add(target, np.multiply(self.wander_radius, orientation_scalar_to_vector(target_orientation)))
        self.face.set_temporary_target(target)
        steering = self.face.get_steering()
        if steering == None: return None
        steering.linear = np.multiply(self.max_acceleration, orientation_scalar_to_vector(self.character.orientation))
        return steering

class VelocityMatch:
    character = Kinematic()
    target = Kinematic()
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
        pass

class Pursue(Seek):
    max_prediction = 0.5
    temporary_target = Kinematic()
    seek = Seek()

    def __init__(self):
        pass

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
    radius = 12
    time = 0.03
    kinematic = Kinematic()
    steering = SteeringOutput()
    kinematic_arrive = KinematicArrive() 
    kinematic_wander = KinematicWander()
    seek = Seek()
    arrive = Arrive()
    pursue = Pursue()
    align = Align()
    face = Face()
    wander = Wander()

    def __init__(self):
        pass
    
    def draw(self):
        pygame.draw.circle(window, self.color, self.wander.character.position, self.radius)

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
    #     self.kinematic.update(self.steering, 10.0, self.time)

    # #steering behaviors: seek
    # def update(self, target_center):
    #     self.seek.target.position = target_center
    #     self.seek.character.update(self.seek.get_steering(), 0.6, self.time)

    #steering behaviors: arrive
    # def update(self, target_center):
    #     # self.arrive.update_character(self.kinematic.position, self.kinematic.orientation)
    #     # self.arrive.target.position = [0.0, 0.0]
    #     target = Kinematic()
    #     target.position = target_center
    #     # if self.arrive.get_steering() != None:
    #         # self.kinematic.velocity = self.kinematic_arrive.get_steering().velocity
    #         # self.kinematic.rotation = self.kinematic_arrive.get_steering().rotation
    #     self.arrive.character.update(self.arrive.get_steering(target), 0.1, self.time)

    #steering behaviors: pursue(seek)
    # def update(self, target_center):
        # self.pursue.set_temporary_target(target_center)
        # self.pursue.character.update(self.pursue.get_steering(), 0.6, self.time)

    # # steering behaviors: align
    # def update(self, target):
    #     # print("XD = ", self.wander.get_steering().angular)
    #     # print(" ")
    #     self.align.set_target_orientation(target)
    #     if self.align.get_steering(target) != None:
    #         self.align.character.update(self.align.get_steering(target), 0.6, self.time)
    #     # print(self.align.character.orientation)
    #     # print("FINAL angular = ", self.align.get_steering(target).angular)
    #     # print("\n")

    # # steering behaviors: face
    # def update(self, target):
    #     self.face.set_temporary_target(target)
    #     self.face.get_steering()
    #     print(" ")
    #     # if self.align.get_steering(target) != None:
    #         # self.align.character.update(self.align.get_steering(target), 0.6, self.time)
    #     # print(self.align.character.orientation)
    #     # print("FINAL angular = ", self.align.get_steering(target).angular)
    #     # print("\n")

    # steering behaviors: wander
    def update(self):
        self.wander.character.update(self.wander.get_steering(), 10.6, self.time)
