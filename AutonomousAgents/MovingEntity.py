from turtle import position
import numpy as np
import pygame
from math import *
import time

class BaseGameEntity():
    position = [100.0, 400.0]

    def __init__(self, position):
        self.position = position


# class GameWorld():
#     def __init__(self):
#         pass

class MovingEntity(BaseGameEntity):
    velocity = [1.0, 0.0]
    heading = [0.0, 0.0]
    side = [0.0, 0.0]
    mass = 10.0
    max_speed = 10.0
    max_force = 10.0
    max_turn_rate = 10.0

    def __init__(self, velocity, heading, side, mass, max_speed, max_force, max_turn_rate):
        self.velocity = velocity
        self.heading = heading
        self.side = side
        self.mass = mass
        self.max_speed = max_speed
        self.max_force = max_force
        self.max_turn_rate = max_turn_rate


class SteeringBehaviors():
    steering_force = [0.0, 0.0]
    desired_velocity = [0.0, 0.0]
    vehicle_position = [0.0, 0.0]
    vehicle_velocity = [0.0, 0.0]
    vehicle_max_speed = 0.0

    def __init__(self, vehicle_position, vehicle_max_speed, vehicle_velocity):
        self.vehicle_position = vehicle_position
        self.vehicle_max_speed = vehicle_max_speed
        self.vehicle_velocity = vehicle_velocity

    def calculate(self):
        steering_force = [1.0, 0.0]    
        return steering_force
        #TODO

    def seek(self, target_position):
        self.desired_velocity = np.multiply(normalize(np.subtract(target_position, self.vehicle_position)), self.vehicle_max_speed)
        return np.subtract(self.desired_velocity, )

class Vehicle(MovingEntity):
    steering_behaviors = SteeringBehaviors(self.position, self.max_speed, self.velocity)
    steering_force = [0.0, 0.0]
    acceleration = [0.0, 0.0]

    def __init__(self):
        pass

    def update(self, time_elapsed):
        self.steering_force = self.steering_behaviors.calculate()
        self.acceleration = [x / self.mass for x in self.steering_force]
        self.velocity += np.multiply(self.acceleration, time_elapsed)
        
        # //make sure vehicle does not exceed maximum velocity
        # m_vVelocity.Truncate(m_dMaxSpeed);
        #?!!!!!!!!!!!!
        if np.linalg.norm(self.velocity) > self.max_force:
            print("TRUNCATE TODO!!!!")

        self.position += np.multiply(self.velocity, time_elapsed)

        if np.linalg.norm(self.velocity) > 0.0000001:
            self.heading = (self.velocity / np.linalg.norm(self.velocity))
            self.side = perp(self.heading)

    def draw(self):
        pygame.draw.circle(window, (0, 255, 0), self.position, 15)


# class Vehicle(MovingEntity):
#     game_world = GameWorld()
#     steering_behaviors = SteeringBehaviors()
#     steering_force = [0.0, 0.0]
#     acceleration = [0.0, 0.0]

#     def __init__(self):
#         pass

#     def draw(self):
#         pygame.draw.circle(window, (0, 255, 0), self.velocity, 15)

#     def update(self, time_elapsed):
#         self.steering_force = self.steering_behaviors.calculate()
#         self.acceleration = np.divide(self.steering_force, self.mass)
#         self.velocity += np.multiply(self.acceleration, time_elapsed)

#         if np.linalg.norm(self.velocity) > 0.0000001:
#             self.heading = (self.velocity / np.linalg.norm(self.velocity)) #????
#             self.side = perp(self.heading)

#         #//treat the screen as a toroid
#         #WrapAround(m_vPos, m_pWorld->cxClient(), m_pWorld->cyClient());
#         # WTF XDDDDDDDD

def perp(v1):
    #nie moglem znalezc sensowengo w numpy
    v2 = [0.0, 0.0]
    v2[0] = v1[1]
    v2[1] = - v1[0]
    return v2

def normalize(vec):
    help = vec / np.linalg.norm(vec)
    return help

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
vehicle = Vehicle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # time.sleep(1)
    window.fill((0, 0, 0))
    vehicle.draw()
    vehicle.update(0.03)
    pygame.draw.polygon(window, (255, 0, 0), [(100, 100), (50, 150), (150, 150)], 0)
    pygame.display.update()
