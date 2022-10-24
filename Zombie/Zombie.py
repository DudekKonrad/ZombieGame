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

    target_position = [800.0, 700.0]
    max_speed = 10.0
    target_radius = 0.5
    time_to_target = 0.25

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
        
        #rysowanie celu do ktorego zmierza zombiak (tylko pomocniczo, potem wyleci)
        pygame.draw.circle(window, (0,0,255), self.target_position, self.radius)

    def kinematic_update(self):
        self.position += np.multiply(self.velocity, self.time)
        self.orientation += self.rotation * self.time

        self.velocity += np.multiply(self.steering_linear, self.time)
        self.orientation += self.steering_angular * self.time

    # def get_new_orientation(self):
        #TODO
        #skierowanie sie czubkiem zombiaka w kierunku celu
        #w przypadku okregu CHYBA niepotrzebne

    def kinematic_arrive(self):
        self.velocity = np.subtract(self.target_position, self.position)
        if np.linalg.norm(self.velocity) < self.target_radius:
            return #???
        else:
            self.velocity = np.divide(self.velocity, self.time_to_target)

            if np.linalg.norm(self.velocity) > self.max_speed:
                normalized_velocity = self.velocity / np.linalg.norm(self.velocity)
                self.velocity = normalized_velocity
                self.velocity = np.multiply(self.velocity, self.max_speed)
            
            #face direction get_new_orientation()
            self.rotation = 0.0
