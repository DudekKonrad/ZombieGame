import random
import numpy as np
import pygame.time
from numpy.linalg import norm

from Variables.map_variables import *
from Variables.hero_variables import *
from Zombie.Zombie import Zombie


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
    killed_enemies = 0
    shooting_time = 0

    # Temporary Variables:
    old_angle = 0
    correction_angle = 90
    will_collide = False
    shoot_handled = False
    clock = None
    destination_point = (0, 0)

    def __init__(self, coordinates, speed, world):
        self.coordinates = coordinates
        self.future_coordinates = coordinates
        self.speed = speed
        self.collision_circle_r = HERO_HIT_BOX_R
        self.world = world
        self.clock = pygame.time.Clock

    def get_position(self):
        return get_center(self.coordinates)

    def hero_input(self):
        keys = pygame.key.get_pressed()
        self.calculate_angle(pygame.mouse.get_pos())
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
        if keys[pygame.K_s]:
            self.spawn_enemy()

    def hero_shoot(self):
        time_since_enter = pygame.time.get_ticks() - self.shooting_time
        if time_since_enter <= SHOOTING_COOLDOWN:
            self.draw_shoot(self.destination_point)
            return
        center = get_center(self.coordinates)
        if pygame.mouse.get_pressed()[0] and self.shoot_handled is False:
            if_hit_obstacle = False
            hit_obstacle = None

            self.shooting_time = pygame.time.get_ticks()

            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            self.destination_point = (mouse_x, mouse_y)
            self.draw_shoot((mouse_x, mouse_y))
            p1 = np.asarray(center)
            p2 = np.asarray(pygame.mouse.get_pos())

            for obstacle in self.world.obstacles:
                p3 = np.asarray(obstacle.coordinates)
                distance_to_obstacle = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
                distance_to_obstacle -= HERO_LASER_SIZE / 2
                if distance_to_obstacle <= obstacle.radius:
                    if mouse_x > center[0] and obstacle.coordinates[0] > center[0]:
                        if_hit_obstacle = True
                        obstacle.color = (123, 154, 21)
                        hit_obstacle = obstacle
                    if mouse_x < center[0] and obstacle.coordinates[0] < center[0]:
                        if_hit_obstacle = True
                        obstacle.color = (123, 154, 21)
                        hit_obstacle = obstacle
                else:
                    obstacle.color = (100, 100, 100)

            for enemy in self.world.enemies:
                p3 = np.asarray(enemy.position)
                distance_to_enemy = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
                distance_to_enemy -= HERO_LASER_SIZE / 2
                if distance_to_enemy <= enemy.radius:
                    if not if_hit_obstacle:
                        if mouse_x > center[0] and enemy.position[0] > center[0]:
                            self.kill_enemy(enemy)
                        if mouse_x < center[0] and enemy.position[0] < center[0]:
                            self.kill_enemy(enemy)

                    if if_hit_obstacle:
                        player_to_obstacle_distance = dist(center, hit_obstacle.coordinates)
                        player_to_enemy_distance = dist(center, enemy.position)
                        if player_to_enemy_distance < player_to_obstacle_distance:
                            if mouse_x > center[0] and enemy.position[0] > center[0]:
                                self.kill_enemy(enemy)
                            if mouse_x < center[0] and enemy.position[0] < center[0]:
                                self.kill_enemy(enemy)

            self.shoot_handled = True
        if not pygame.mouse.get_pressed()[0]:
            self.shoot_handled = False

    def kill_enemy(self, enemy):
        self.world.enemies.remove(enemy)
        self.killed_enemies += 1

    def spawn_enemy(self):
        random_x = random.randint(FRAME_SIZE, SCREEN_WIDTH - FRAME_SIZE)
        random_y = random.randint(FRAME_SIZE, SCREEN_HEIGHT - FRAME_SIZE)
        enemy = Zombie([random_x, random_y])
        self.world.enemies.append(enemy)
        return enemy

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
