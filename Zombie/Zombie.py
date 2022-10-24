from turtle import position
from Variables.global_variables import *
import numpy as np

class Zombie:
    radius = 0
    color = (0, 255, 0)
    time = 0.0
    position = [0.0, 0.0]
    orientation = 0.0
    velocity = [0.0, 0.0]
    rotation = 0.0
    steering_linear = [0.0, 0.0]
    steering_angular = 0.0

    target_position = [0.0, 400.0]
    max_speed = 10.0

    def __init__(self, radius, position, time, orientation, velocity, rotation, steering_linear, steering_angular):
        self.radius = radius
        self.position = position
        self.time = time
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation
        self.steering_linear = steering_linear
        self.steering_angular = steering_angular

    def draw(self):
        pygame.draw.circle(window, self.color, self.position, self.radius)

    def kinematic_update(self):
        self.position += np.multiply(self.velocity, self.time)
        self.orientation += self.rotation * self.time

        self.velocity += np.multiply(self.steering_linear, self.time)
        self.orientation += self.steering_angular * self.time

    # def get_new_orientation(self):
        #TODO
        #skierowanie sie czubkiem zombiaka w kierunku celu
        #w przypadku okregu CHYBA niepotrzebne

    def kinematic_seek(self):
        self.velocity = np.subtract(self.target_position, self.position)
        normalized_velocity = self.velocity / np.linalg.norm(self.velocity)
        self.velocity = normalized_velocity
        self.velocity = np.multiply(self.velocity, self.max_speed)
        #face direction get_new_orientation()
        self.rotation = 0.0
