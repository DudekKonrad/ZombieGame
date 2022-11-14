import numpy as np
import pygame.time
from numpy.linalg import norm

from Variables.global_variables import *
from Variables.map_variables import *
from Variables.hero_variables import *


def get_center(coordinates):
    n = len(coordinates)
    cx = sum(p[0] for p in coordinates) / n
    cy = sum(p[1] for p in coordinates) / n
    return cx, cy


def calculate_laser_direction(player_x, player_y, mouse_x, mouse_y):
    dx = player_x - mouse_x + 0.01
    dy = player_y - mouse_y

    reversed_sign_x = 1 if dx < 0 else -1

    slope = dy / dx

    x_new = reversed_sign_x * SCREEN_WIDTH
    y_new = player_y + slope * (x_new - player_x)

    return x_new, y_new


class Hero:
    coordinates = [(0, 0), (0, 0), (0, 0)]
    speed = 0
    color = HERO_COLOR
    collision_circle_r = 0
    world = None

    # Temporary Variables:
    old_angle = 0
    correction_angle = 0
    will_collide = False
    shoot_handled = False

    def __init__(self, coordinates, speed, world):
        self.coordinates = coordinates
        self.future_coordinates = coordinates
        self.speed = speed
        self.collision_circle_r = 2 / 3 * dist(self.coordinates[0], self.coordinates[1])
        self.world = world

    def hero_input(self):
        keys = pygame.key.get_pressed()
        self.hero_movement(keys)
        self.hero_shoot()

    def hero_movement(self, keys):
        center = get_center(self.coordinates)
        temp = self.coordinates[:]
        if keys[pygame.K_LEFT] and center[0] - self.collision_circle_r > FRAME_SIZE:
            future_position = self.step_left(temp)
            for obstacle in self.world.obstacles:
                if self.check_if_collide(future_position, obstacle):
                    return
            self.step_left(self.coordinates)
        if keys[pygame.K_RIGHT] and center[0] + self.collision_circle_r < SCREEN_WIDTH - FRAME_SIZE:
            future_position = self.step_right(temp)
            for obstacle in self.world.obstacles:
                if self.check_if_collide(future_position, obstacle):
                    return
            self.step_right(self.coordinates)
        if keys[pygame.K_UP] and center[1] - self.collision_circle_r > FRAME_SIZE:
            future_position = self.step_up(temp)
            for obstacle in self.world.obstacles:
                if self.check_if_collide(future_position, obstacle):
                    return
            self.step_up(self.coordinates)
        if keys[pygame.K_DOWN] and center[1] + self.collision_circle_r < SCREEN_HEIGHT - FRAME_SIZE:
            future_position = self.step_down(temp)
            for obstacle in self.world.obstacles:
                if self.check_if_collide(future_position, obstacle):
                    return
            self.step_down(self.coordinates)

    def hero_shoot(self):
        center = get_center(self.coordinates)
        if pygame.mouse.get_pressed()[0] and self.shoot_handled is False:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            self.draw_shoot((mouse_x, mouse_y))
            p1 = np.asarray(center)
            p2 = np.asarray(pygame.mouse.get_pos())

            for obstacle in self.world.obstacles:
                p3 = np.asarray(obstacle.coordinates)
                d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
                if d <= obstacle.radius:
                    obstacle.color = (50, 50, 200)
                else:
                    obstacle.color = (100, 100, 100)
            for enemy in self.world.enemies:
                p3 = np.asarray(enemy.get_character().position)
                d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
                if d <= enemy.radius:
                    enemy.color = (50, 50, 200)
                else:
                    enemy.color = (0, 255, 0)
            self.shoot_handled = False
        if not pygame.mouse.get_pressed()[0]:
            self.shoot_handled = False

    def draw_shoot(self, destination_point):
        end_position = calculate_laser_direction(get_center(self.coordinates)[0], get_center(self.coordinates)[1],
                                                 destination_point[0],
                                                 destination_point[1])
        pygame.draw.line(window, (0, 255, 0), get_center(self.coordinates), end_position, HERO_LASER_SIZE)

    def rotate(self, angle):
        new_points = []
        if self.old_angle == angle:
            return
        for p in self.coordinates:
            center = get_center(self.coordinates)
            tx, ty = p[0] - center[0], p[1] - center[1]
            new_x = (tx * cos(angle) - ty * sin(angle)) + center[0]
            new_y = (tx * sin(angle) + ty * cos(angle)) + center[1]
            new_points.append((new_x, new_y))
        self.old_angle = angle
        self.coordinates = new_points

    def calculate_angle(self, direction):
        dx, dy = direction[0] - get_center(self.coordinates)[0], direction[1] - get_center(self.coordinates)[1]
        angle = degrees(atan2(dy, dx)) - self.correction_angle
        self.rotate(radians(angle))
        self.correction_angle = angle + self.correction_angle

    def draw_hero(self):
        pygame.draw.polygon(window, self.color, self.coordinates, 0)

    def step_left(self, coordinates):
        for i in range(3):
            editable_vertex = list(coordinates[i])
            editable_vertex[0] -= self.speed
            coordinates[i] = tuple(editable_vertex)
        return coordinates

    def step_right(self, coordinates):
        for i in range(3):
            editable_vertex = list(coordinates[i])
            editable_vertex[0] += self.speed
            coordinates[i] = tuple(editable_vertex)
        return coordinates

    def step_up(self, coordinates):
        for i in range(3):
            editable_vertex = list(coordinates[i])
            editable_vertex[1] -= self.speed
            coordinates[i] = tuple(editable_vertex)
        return coordinates

    def step_down(self, coordinates):
        for i in range(3):
            editable_vertex = list(coordinates[i])
            editable_vertex[1] += self.speed
            coordinates[i] = tuple(editable_vertex)
        return coordinates

    def check_if_collide(self, coordinates, obstacle):
        if dist(get_center(coordinates), obstacle.coordinates) <= self.collision_circle_r + obstacle.radius:
            obstacle.color = (255, 190, 92)
            return True
        else:
            obstacle.color = (100, 100, 100)
            return False
