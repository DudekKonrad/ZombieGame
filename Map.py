import random
import pygame.draw
from Obstacle.Obstacle import *
from Variables.map_variables import *
from Variables.obstacle_variables import *
import math


class Map:
    def __init__(self, screen):
        self.screen = None
        self.obstacles = []
        self.enemies = []
        self.screen = screen

    def make_map(self):
        for o in range(OBSTACLES_NUMBER):
            random_radius = random.randint(OBSTACLE_MIN_RADIUS, OBSTACLE_MAX_RADIUS)
            diameter = random_radius*2
            random_x = random.randint(diameter + FRAME_SIZE, SCREEN_WIDTH - FRAME_SIZE - diameter)
            random_y = random.randint(diameter + FRAME_SIZE, SCREEN_HEIGHT - FRAME_SIZE - diameter)
            obstacle_candidate = Obstacle([random_x, random_y], random_radius)

            if self.can_add_obstacle(obstacle_candidate):
                self.obstacles.append(obstacle_candidate)

    def draw_map(self):
        pygame.draw.rect(window, FRAME_COLOR, [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], FRAME_SIZE-5)
        for obstacle in self.obstacles:
            obstacle.draw_obstacle(window)

    def can_add_obstacle(self, obstacle_to_add):
        can_add = True
        for obstacle in self.obstacles:
            dist = math.dist(obstacle.coordinates, obstacle_to_add.coordinates)
            if dist < int(obstacle.radius * 4):
                can_add = False
        return can_add

    def get_obstacle_position(self, num):
        return self.obstacles[num].coordinates

    def get_nearest_obstacle(self, point):
        dist = 0.0
        pom_obstacle = [0.0, 0.0]
        counter = 0
        for obstacle in self.obstacles:
            pom_obstacle = obstacle.coordinates
            # print(pom_obstacle)
            # dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
            dist = math.sqrt( math.pow(point[0] - pom_obstacle[0], 2) + math.pow(point[1] - pom_obstacle[1], 2))
            if dist < 100:
                return counter
            counter = counter + 1
        return -1
