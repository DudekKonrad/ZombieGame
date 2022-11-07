from Variables.global_variables import *
from math import *
from Variables.map_variables import *


class Hero:
    coordinates = [(0, 0), (0, 0), (0, 0)]
    size = [0, 0]
    speed = 0
    color = (255, 0, 0)
    old_angle = 0
    correction_angle = 0
    collision_circle_r = 0

    def __init__(self, coordinates, size, speed):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.collision_circle_r = 2/3*dist(self.coordinates[0], self.coordinates[1])

    def get_collision_circle_r(self):
        h = dist(self.coordinates[0], self.coordinates[1])
        return 2/3*h

    def hero_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.get_center()[0]-self.collision_circle_r > FRAME_SIZE:
            self.step_left()
        if keys[pygame.K_RIGHT] and self.get_center()[0] + self.collision_circle_r < SCREEN_WIDTH - FRAME_SIZE:
            self.step_right()
        if keys[pygame.K_UP] and self.get_center()[1]-self.collision_circle_r > FRAME_SIZE:
            self.step_up()
        if keys[pygame.K_DOWN] and self.get_center()[1]+self.collision_circle_r < SCREEN_HEIGHT-FRAME_SIZE:
            self.step_down()

    def get_center(self):
        n = len(self.coordinates)
        cx = sum(p[0] for p in self.coordinates) / n
        cy = sum(p[1] for p in self.coordinates) / n
        return cx, cy

    def rotate(self, angle):
        new_points = []
        if self.old_angle == angle:
            return
        for p in self.coordinates:
            tx, ty = p[0] - self.get_center()[0], p[1] - self.get_center()[1]
            new_x = (tx * cos(angle) - ty * sin(angle)) + self.get_center()[0]
            new_y = (tx * sin(angle) + ty * cos(angle)) + self.get_center()[1]
            new_points.append((new_x, new_y))
        self.old_angle = angle
        self.coordinates = new_points

    def calculate_angle(self, direction):
        dx, dy = direction[0] - self.get_center()[0], direction[1] - self.get_center()[1]
        angle = degrees(atan2(dy, dx)) - self.correction_angle
        self.rotate(radians(angle))
        self.correction_angle = angle + self.correction_angle

    def draw_hero(self):
        self.hero_movement()
        window.fill((0, 0, 0))  # odswiezenie ekranu
        pygame.draw.polygon(window, self.color, self.coordinates, 0)

    def step_left(self):
        for i in range(3):
            editable_vertex = list(self.coordinates[i])
            editable_vertex[0] -= self.speed
            self.coordinates[i] = tuple(editable_vertex)

    def step_right(self):
        for i in range(3):
            editable_vertex = list(self.coordinates[i])
            editable_vertex[0] += self.speed
            self.coordinates[i] = tuple(editable_vertex)

    def step_up(self):
        for i in range(3):
            editable_vertex = list(self.coordinates[i])
            editable_vertex[1] -= self.speed
            self.coordinates[i] = tuple(editable_vertex)

    def step_down(self):
        for i in range(3):
            editable_vertex = list(self.coordinates[i])
            editable_vertex[1] += self.speed
            self.coordinates[i] = tuple(editable_vertex)

    def check_if_collide(self, obstacle):
        if dist(self.get_center(), obstacle.coordinates) <= self.get_collision_circle_r()+obstacle.radius:
            obstacle.color = (255, 190, 92)
        else:
            obstacle.color = (100, 100, 100)

