import math
import pygame.draw
import numpy as np
import random

from pygame import Vector2
from Variables.map_variables import *
from Variables.zombie_variables import *


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


def getNewOrientation(orientation, velocity):
    if velocity.length() > 0:
        return math.atan2(-velocity[0], velocity[1])
    else:
        return orientation


def get_hide_coordinates(hero_coordinates, obstacle_coordinates):
    hero_coordinates = list(hero_coordinates)
    obstacle_to_hero = [0, 0]
    hide_coordinates = [0, 0]

    # wektor od zaslony do gracza
    obstacle_to_hero[0] = hero_coordinates[0] - obstacle_coordinates[0]
    obstacle_to_hero[1] = hero_coordinates[1] - obstacle_coordinates[1]

    # wektor przeciwny
    obstacle_to_hero[0] = - obstacle_to_hero[0]
    obstacle_to_hero[1] = - obstacle_to_hero[1]

    # wektor jednostkowy
    vector_length = math.sqrt(pow(obstacle_to_hero[0], 2) + pow(obstacle_to_hero[1], 2))
    obstacle_to_hero[0] = (OBSTACLE_MAX_RADIUS + 10) * (obstacle_to_hero[0] / vector_length)
    obstacle_to_hero[1] = (OBSTACLE_MAX_RADIUS + 10) * (obstacle_to_hero[1] / vector_length)

    hide_coordinates[0] = obstacle_coordinates[0] + obstacle_to_hero[0]
    hide_coordinates[1] = obstacle_coordinates[1] + obstacle_to_hero[1]

    return hide_coordinates


class Static:

    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation


class Kinematic:

    def __init__(self, position):
        self.position = Vector2(position)
        self.orientation = 0.0
        self.velocity = Vector2(1, 1)
        self.rotation = 0
        self.angle = 0
        pass

    def update(self, steering, max_speed, my_time):
        # Velocity before changes
        if steering is not None:
            self.position = self.position + self.velocity * my_time
            self.orientation = self.orientation + self.rotation * my_time

            self.velocity = self.velocity + steering.linear * my_time
            # self.orientation = getNewOrientation(self.orientation, self.velocity)
            self.rotation = self.rotation + steering.angular * my_time

            if self.velocity.length() > max_speed:
                self.velocity = self.velocity.normalize()
                self.velocity = self.velocity * max_speed

        # Show velocity vector
        # pygame.draw.line(window, (0, 0, 255), self.position, self.position + self.velocity, 1)

        # Show orientation
        # vec = pygame.math.Vector2(0, 100).rotate(self.angle)
        # pt_x, pt_y = self.position[0] + vec.x, self.position[1] + vec.y
        # new_o = getNewOrientation(self.rotation, self.velocity)
        # self.angle = math.degrees(new_o)
        # pygame.draw.line(window, (110, 10, 155), self.position, (pt_x, pt_y), 2)


class SteeringOutput:

    def __init__(self):
        self.linear = Vector2(0, 0)
        self.angular = 0
        pass


class Seek:

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = self.target.position - self.character.position
        steering.linear = steering.linear.normalize()
        steering.linear = steering.linear * self.character.max_acceleration
        self.character.orientation = getNewOrientation(self.character.orientation, steering.linear)
        steering.angular = 0.0

        return steering


class Flee:

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = self.character.position - self.target.position
        steering.linear = steering.linear.normalize()
        steering.linear = steering.linear * self.character.max_acceleration
        steering.angular = 0.0
        return steering


class Arrive:

    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.target_radius = 10
        self.slow_radius = 0.0
        self.time_to_target = 0.1

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def get_steering(self):
        steering = SteeringOutput()
        direction = self.target.position - self.character.position
        distance = direction.length()
        if distance < self.target_radius:
            return None
        if distance > self.slow_radius:
            target_speed = self.character.max_acceleration
        else:
            target_speed = self.character.max_speed * distance / self.slow_radius
        target_velocity = direction
        target_velocity = target_velocity.normalize()
        target_velocity = target_velocity * target_speed

        steering.linear = target_velocity - self.character.velocity
        steering.linear = steering.linear / self.time_to_target

        if steering.linear.length() > self.character.max_acceleration:
            steering.linear = steering.linear.normalize()
            steering.linear = steering.linear * self.character.max_acceleration

        steering.angular = 0.0
        return steering


class Wander(Seek):
    circle_pos = [50, 50]
    wander_ring_distance = 400

    def get_steering(self):
        if self.character.velocity.length() == 0: return
        self.circle_pos = self.get_circle_pos()
        target_pos = self.circle_pos + pygame.math.Vector2(self.wander_ring_distance, 0).rotate(random.uniform(0, 360))
        self.target = Static(target_pos, 0)
        return Seek.get_steering(self)

    def get_circle_pos(self):
        x = self.character.position + self.character.velocity.normalize() * self.wander_ring_distance
        return x


def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in
                                      intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(
                discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def line_intersection(line1, line2):
    x1 = float(line1[0][0])
    y1 = float(line1[0][1])
    x2 = float(line1[1][0])
    y2 = float(line1[1][1])

    x3 = float(line2[0][0])
    y3 = float(line2[0][1])
    x4 = float(line2[1][0])
    y4 = float(line2[1][1])

    m = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if m != 0:
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / m
        u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / m
        x, y = (x1 + t * (x2 - x1)), (y1 + t * (y2 - y1))
        if 0 <= t <= 1 and 0 <= u <= 1:
            return x, y
        else:
            return None


def get_normal_vector_down(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    dx = x2 - x1
    dy = y2 - y1
    return Vector2(-dy, dx)


def get_normal_vector_up(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    dx = x2 - x1
    dy = y2 - y1
    return Vector2(dy, -dx)


class Collision:

    def __init__(self, collide_point, normal):
        self.position = Vector2(collide_point)
        self.normal = Vector2(normal)


class Collision_Detector:
    def get_collision(self, position, move_amount):
        # Collision with walls
        top_collision = line_intersection(TOP_BORDER, (position, position + move_amount))
        left_collision = line_intersection(LEFT_BORDER, (position, position + move_amount))
        right_collision = line_intersection(RIGHT_BORDER, (position, position + move_amount))
        bottom_collision = line_intersection(BOTTOM_BORDER, (position, position + move_amount))
        if top_collision is not None:
            normal_vector = get_normal_vector_down(TOP_BORDER)
            collision = Collision(top_collision, normal_vector)
            return collision
        if right_collision is not None:
            normal_vector = get_normal_vector_down(RIGHT_BORDER)
            collision = Collision(right_collision, normal_vector)
            return collision
        if left_collision is not None:
            normal_vector = get_normal_vector_up(LEFT_BORDER)
            collision = Collision(left_collision, normal_vector)
            return collision
        if bottom_collision is not None:
            normal_vector = get_normal_vector_up(BOTTOM_BORDER)
            collision = Collision(bottom_collision, normal_vector)
            return collision


class ObstacleAvoidance(Seek):

    def __init__(self, character, target, obstacles):
        super().__init__(character, target)
        self.collision_detector = Collision_Detector()
        self.obstacles = obstacles

    def get_steering(self):
        ray_vector = self.character.velocity
        ray_vector = ray_vector.normalize()
        ray_vector *= self.character.look_ahead

        # Show ray vector
        # pygame.draw.line(window, (255, 255, 255), self.character.position, self.character.position + ray_vector, 2)

        # Collision with walls
        collision = self.collision_detector.get_collision(self.character.position, ray_vector)
        if collision is not None:
            self.target.position = collision.position + collision.normal * self.character.avoid_distance

        # Collision with obstacles
        for obstacle in self.obstacles:
            circle_collision = circle_line_segment_intersection(obstacle.coordinates, obstacle.radius,
                                                                self.character.position,
                                                                self.character.position + ray_vector, False)
            if len(circle_collision) > 0:
                # pygame.draw.circle(window, (1, 24, 222), circle_collision[0], 5)
                end = (self.character.position, circle_collision[0])
                n = get_normal_vector_up(end)
                target_pos = circle_collision[0] + n * self.character.avoid_distance
                self.target.position = target_pos
        return Seek.get_steering(self)


class ObstacleAvoidanceWander(Wander):

    def __init__(self, character, target, obstacles):
        super().__init__(character, target)
        self.collision_detector = Collision_Detector()
        self.obstacles = obstacles

    def get_steering(self):
        ray_vector = self.character.velocity
        ray_vector = ray_vector.normalize()
        ray_vector *= self.character.look_ahead
        pygame.draw.line(window, (255, 255, 255), self.character.position, self.character.position + ray_vector, 2)

        # Collision with walls
        collision = self.collision_detector.get_collision(self.character.position, ray_vector)
        if collision is not None:
            target_pos = collision.position + collision.normal * self.character.avoid_distance
            self.target = Static(target_pos, 0)
            return Seek.get_steering(self)

        # Collision with obstacles
        for obstacle in self.obstacles:
            circle_collision = circle_line_segment_intersection(obstacle.coordinates, obstacle.radius,
                                                                self.character.position,
                                                                self.character.position + ray_vector, False)
            if len(circle_collision) > 0:
                pygame.draw.circle(window, (1, 24, 222), circle_collision[0], 5)
                end = (self.character.position, circle_collision[0])
                normal_vector = get_normal_vector_up(end)
                target_pos = circle_collision[0] + normal_vector * self.character.avoid_distance
                self.target = Static(target_pos, 0)
                return Seek.get_steering(self)

        return Wander.get_steering(self)


class Separation(ObstacleAvoidanceWander):

    def __init__(self, character, target, obstacles, targets):
        super().__init__(character, target, obstacles)
        self.targets = targets
        self.threshold = 35
        self.decay_coefficient = 10000
        self.max_acceleration = 1000

    def get_steering(self):
        steering = SteeringOutput()
        for target in self.targets:
            direction = target.position - self.character.position
            distance = direction.length()
            pygame.draw.circle(window, (0, 0, 255), self.character.position, self.threshold, 1)
            if distance < self.threshold:
                # print(f"Distance {distance} < threshold: {self.threshold}")
                self.character.color = (255, 0, 0)
                strength = min(self.decay_coefficient / (distance * distance), self.max_acceleration)
                direction = direction.normalize()
                steering.linear -= strength * direction
            else:
                self.character.color = ZOMBIE_COLOR
                return ObstacleAvoidanceWander.get_steering(self)
        return steering


class Separation2(ObstacleAvoidance):

    def __init__(self, character, target, obstacles, targets):
        super().__init__(character, target, obstacles)
        self.targets = targets
        self.threshold = 35
        self.decay_coefficient = 10000
        self.max_acceleration = 1000

    def get_steering(self):
        steering = SteeringOutput()
        for target in self.targets:
            direction = target.position - self.character.position
            distance = direction.length()
            pygame.draw.circle(window, (0, 0, 255), self.character.position, self.threshold, 1)
            if distance < self.threshold:
                print(f"Distance {distance} < threshold: {self.threshold}")
                self.character.color = (255, 0, 0)
                strength = min(self.decay_coefficient / (distance * distance), self.max_acceleration)
                direction = direction.normalize()
                steering.linear -= strength * direction
            else:
                self.character.color = ZOMBIE_COLOR
                return ObstacleAvoidance.get_steering(self)
        return steering


class CollisionAvoidance(ObstacleAvoidanceWander):

    def __init__(self, character, target, targets, obstacles):

        super().__init__(character, target, obstacles)
        self.targets = targets
        self.radius = 8

    def get_steering(self):
        shortest_time = float('inf')
        first_target = None
        first_min_separation = None
        first_relative_pos = None
        first_relative_vel = None
        steering = SteeringOutput()
        for target in self.targets:
            first_target = None
            relative_pos = target.position - self.character.position
            relative_vel = target.velocity - self.character.velocity + Vector2(0.00001, 0)
            relative_speed = relative_vel.length()
            time_to_collision = (relative_pos.dot(relative_vel)) / (relative_speed * relative_speed)
            distance = relative_pos.length()
            min_separation = distance - relative_speed * shortest_time
            if min_separation > 2 * self.radius:
                continue
            if 0 < time_to_collision < shortest_time:
                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_relative_pos = relative_pos
                first_relative_vel = relative_vel
            if not first_target:
                return ObstacleAvoidanceWander.get_steering(self)
            if first_min_separation <= 0 or distance < 2 * self.radius:
                relative_pos = first_target.position - self.character.position
                self.character.color = (255, 0, 0)
            else:
                self.character.color = ZOMBIE_COLOR
                relative_pos = first_relative_pos + first_relative_vel * shortest_time
            relative_pos = relative_pos.normalize()
            steering.linear = -relative_pos * self.character.max_acceleration
            return steering

        return ObstacleAvoidanceWander.get_steering(self)


class Zombie(Kinematic):
    steering = None
    target = None
    max_acceleration = 40
    radius = ZOMBIE_RADIUS
    other_zombies = []
    obstacles = []
    avoid_distance = 1000
    look_ahead = 50
    color = ZOMBIE_COLOR
    time_counter = 0
    how_long_zombie_will_stay_behind_obstacle = 9000 #2000 means time_counter = 2000 will trigger lefting obstacle

    def set_target(self, target_position):
        self.target = Static(target_position, 0)

    def set_kinematic_target(self, target):
        self.target = target

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles

    def set_steering(self, option):
        if option == "Seek":
            self.steering = Seek(self, self.target)
        elif option == "Flee":
            self.steering = Flee(self, self.target)
        elif option == "Arrive":
            self.steering = Arrive(self, self.target)
        elif option == "Wander":
            self.steering = Wander(self, self.target)
        elif option == "Obstacle_Avoidance":
            self.steering = ObstacleAvoidance(self, self.target, self.obstacles)
        elif option == "Obstacle_Avoidance_Wander":
            self.steering = ObstacleAvoidanceWander(self, self.target, self.obstacles)
        elif option == "Separation":
            self.steering = Separation(self, self.target, self.obstacles, self.other_zombies)
        elif option == "Separation2":
            self.steering = Separation2(self, self.target, self.obstacles, self.other_zombies)
        elif option == "Collision_Avoidance":
            self.steering = CollisionAvoidance(self, self.target, self.other_zombies, self.obstacles)

    def run(self):
        self.update(self.steering.get_steering(), ZOMBIE_MAX_SPEED, ZOMBIE_TIME)
        self.draw()

    def draw(self):
        pygame.draw.circle(window, self.color, self.position, ZOMBIE_RADIUS)

    def set_other_zombies(self):
        temp_zombies = []
        for zombie in self.other_zombies:
            if zombie is not self:
                temp_zombies.append(zombie)
        self.other_zombies = temp_zombies

    def count_nearby_zombies(self, threshold):
        counter = 0
        for z in self.other_zombies:
            if self.position.distance_to(z.position) <= threshold:
                counter += 1
        return counter

    def get_position(self):
        return self.position

    def change_to_left_obstacle_color(self):
        self.color = (100, 0, 105)

    def change_to_attack_color(self):
        self.color = (255, 0, 0)

    def set_obstacle_left_value(self):
        self.how_long_zombie_will_stay_behind_obstacle = random.randint(1000, 3000)
