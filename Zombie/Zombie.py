import math
import pygame.draw
import numpy as np
import random
from Variables.map_variables import *
from Variables.zombie_variables import *
from numpy.linalg import norm


def length(vector):
    return np.linalg.norm(vector)


def normalize(vector):
    return np.divide(vector, length(vector))


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


class Static:
    position = [0.0, 0.0]
    orientation = 0.0

    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation


def getNewOrientation(orientation, velocity):
    if length(velocity) > 0:
        return math.atan2(-velocity[0], velocity[1])
    else:
        return orientation


class Kinematic:
    position = [1.0, 1.0]
    orientation = 0.0
    velocity = [1.0, 0.0]
    rotation = 0.0
    angle = 0

    def __init__(self, position):
        self.position = position
        pass

    def update(self, steering, max_speed, my_time):
        # Velocity before changes
        #
        if steering is not None:
            self.position = np.add(self.position, np.multiply(self.velocity, my_time))
            self.orientation = np.add(self.orientation, np.multiply(self.rotation, my_time))

            self.velocity = np.add(self.velocity, np.multiply(steering.linear, my_time))
            # self.orientation = getNewOrientation(self.orientation, self.velocity)
            self.rotation = np.add(self.rotation, np.multiply(steering.angular, my_time))

            if length(self.velocity) > max_speed:
                self.velocity = normalize(self.velocity)
                self.velocity = np.multiply(self.velocity, max_speed)

        # Drawing velocity vector
        pygame.draw.line(window, (0, 0, 255), self.position, self.position + self.velocity, 2)

        # Drawing orientation
        # vec = pygame.math.Vector2(0, 100).rotate(self.angle)
        # pt_x, pt_y = self.position[0] + vec.x, self.position[1] + vec.y
        # new_o = getNewOrientation(self.rotation, self.velocity)
        # self.angle = math.degrees(new_o)
        # pygame.draw.line(window, (110, 10, 155), self.position, (pt_x, pt_y), 2)


class SteeringOutput:
    linear = [0, 0]
    angular = 0

    def __init__(self):
        pass


class Seek:
    character = None
    target = None

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.target.position, self.character.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.character.max_acceleration)
        self.character.orientation = getNewOrientation(self.character.orientation, steering.linear)
        steering.angular = 0.0

        return steering


class Flee:
    character = None
    target = None

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        steering.linear = np.subtract(self.character.position, self.target.position)
        steering.linear = normalize(steering.linear)
        steering.linear = np.multiply(steering.linear, self.character.max_acceleration)
        steering.angular = 0.0
        return steering


class Arrive:
    character = None
    target = None
    target_radius = 10
    slow_radius = 0.0
    time_to_target = 0.1

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def update_character(self, position, orientation):
        self.character.position = position
        self.character.orientation = orientation

    def get_steering(self):
        steering = SteeringOutput()
        direction = np.subtract(self.target.position, self.character.position)
        distance = length(direction)
        if distance < self.target_radius:
            return None
        if distance > self.slow_radius:
            target_speed = self.character.max_speed
        else:
            target_speed = np.divide(np.multiply(self.character.max_speed, distance), self.slow_radius)
        target_velocity = direction
        target_velocity = normalize(target_velocity)
        target_velocity = np.multiply(target_velocity, target_speed)

        steering.linear = np.subtract(target_velocity, self.character.velocity)
        steering.linear = np.divide(steering.linear, self.time_to_target)

        if length(steering.linear) > self.character.max_acceleration:
            steering.linear = normalize(steering.linear)
            steering.linear = np.multiply(steering.linear, self.character.max_acceleration)

        steering.angular = 0.0
        return steering


class Align:
    character = None
    target = None
    max_angular_acceleration = 10.8
    max_rotation = 900.6
    target_radius = 0.1
    slow_radius = 0.2
    time_to_target = 0.7

    def __init__(self, character, target):
        self.character = character
        self.target = target

    def get_steering(self):
        steering = SteeringOutput()
        rotation = np.subtract(self.target.orientation, self.character.orientation)
        rotation = map_to_range(rotation)
        rotation_size = abs(rotation)

        if rotation_size < self.target_radius:
            return None

        if rotation_size > self.slow_radius:
            target_rotation = self.max_rotation
        else:
            target_rotation = np.divide(np.multiply(self.max_rotation, rotation_size), self.slow_radius)

        target_rotation = np.multiply(target_rotation, np.divide(rotation, rotation_size))
        steering.angular = np.subtract(target_rotation, self.character.rotation)
        steering.angular = np.divide(steering.angular, self.time_to_target)

        angular_acceleration = abs(steering.angular)
        if angular_acceleration > self.max_angular_acceleration:
            steering.angular = np.divide(steering.angular, angular_acceleration)
            steering.angular = np.divide(steering.angular, self.max_angular_acceleration)

        steering.linear = 0.0
        return steering


class Wander(Seek):
    circle_pos = [50, 50]
    wander_ring_distance = 400

    def get_steering(self):
        self.circle_pos = self.get_circle_pos()
        target_pos = np.add(self.circle_pos,
                            pygame.math.Vector2(self.wander_ring_distance, 0).rotate(random.uniform(0, 360)))
        self.target = Static(target_pos, 0)
        return Seek.get_steering(self)

    def get_circle_pos(self):
        x = np.add(self.character.position, np.multiply(normalize(self.character.velocity), self.wander_ring_distance))
        return x


class Separation:
    character = None
    targets = []
    actual_steering = None
    threshold = 10.5
    decay_coefficient = 0.6
    max_acceleration = 4.0

    def __init__(self, character, targets, steering):
        self.character = character
        self.targets = targets
        self.actual_steering = steering

    def get_steering(self):
        steering = SteeringOutput()
        for target in self.targets:
            direction = np.subtract(target.position, self.character.position)
            distance = length(direction)
            if distance < self.threshold:
                strength = min(np.divide(self.decay_coefficient, np.multiply(distance, distance)),
                               self.max_acceleration)
                direction = normalize(direction)
                steering.linear = np.add(steering.linear, np.multiply(strength, direction))
        return steering


class Separation_Wander:
    character = None
    target = None
    other_targets = None
    circle_pos = [0, 0]
    wander_ring_distance = 2
    threshold = 100
    decay_coefficient = 2000
    max_acceleration = 10.0

    def __init__(self, character, targets):
        self.character = character
        self.other_targets = targets

    def get_steering(self):
        self.circle_pos = self.get_circle_pos()
        target_pos = self.circle_pos + pygame.math.Vector2(self.wander_ring_distance, 0).rotate(random.uniform(0, 360))
        self.target = Static(target_pos, 0)
        seek = Seek(self.character, self.target)
        steering = SteeringOutput()
        for target in self.other_targets:
            direction = np.subtract(target.position, self.character.position)
            distance = length(direction)
            if distance < self.threshold:
                self.character.color = (255, 0, 0)
                self.target.color = (255, 10, 100)
                strength = min(np.divide(self.decay_coefficient, np.multiply(distance, distance)),
                               self.max_acceleration)
                direction = normalize(direction)
                seek.get_steering().linear = np.add(steering.linear, np.multiply(strength, direction))
                return seek.get_steering()
        return seek.get_steering()

    def get_circle_pos(self):
        x = np.add(self.character.position, np.multiply(normalize(self.character.velocity), self.wander_ring_distance))
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
            pygame.draw.circle(window, (100, 100, 255), (x, y), 6)
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
    return -dy, dx


def get_normal_vector_up(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    dx = x2 - x1
    dy = y2 - y1
    return dy, -dx


class Collision:
    position = None
    normal = None

    def __init__(self, collide_point, normal):
        self.position = collide_point
        self.normal = normal


class Collision_Detector:
    def get_collision(self, position, move_amount):
        top_collision = line_intersection(TOP_BORDER, (position, position + move_amount))
        left_collision = line_intersection(LEFT_BORDER, (position, position + move_amount))
        right_collision = line_intersection(RIGHT_BORDER, (position, position + move_amount))
        bottom_collision = line_intersection(BOTTOM_BORDER, (position, position + move_amount))
        if top_collision is not None:
            normal_vector = get_normal_vector_down(TOP_BORDER)
            # pygame.draw.line(window, (233, 32, 111), top_collision, normal_vector, 2)
            collision = Collision(top_collision, normal_vector)
            return collision
        if right_collision is not None:
            normal_vector = get_normal_vector_down(RIGHT_BORDER)
            # pygame.draw.line(window, (233, 32, 111), right_collision, normal_vector, 2)
            collision = Collision(right_collision, normal_vector)
            return collision
        if left_collision is not None:
            normal_vector = get_normal_vector_up(LEFT_BORDER)
            # pygame.draw.line(window, (233, 32, 111), left_collision, normal_vector, 2)
            collision = Collision(left_collision, normal_vector)
            return collision
        if bottom_collision is not None:
            normal_vector = get_normal_vector_up(BOTTOM_BORDER)
            # pygame.draw.line(window, (233, 32, 111), bottom_collision, normal_vector, 2)
            collision = Collision(bottom_collision, normal_vector)
            return collision


class ObstacleAvoidance(Seek):
    collision_detector = Collision_Detector()
    obstacles = []

    def __init__(self, character, target, obstacles):
        super().__init__(character, target)
        self.obstacles = obstacles

    def get_steering(self):
        ray_vector = self.character.velocity
        ray_vector = normalize(ray_vector)
        ray_vector *= self.character.look_ahead
        pygame.draw.line(window, (255, 255, 255), self.character.position, self.character.position + ray_vector, 4)

        # Collision with walls
        collision = self.collision_detector.get_collision(self.character.position, ray_vector)
        if collision is not None:
            self.target.position = np.add(collision.position,
                                          np.multiply(collision.normal, self.character.avoid_distance))
        # Collision with obstacles NEED FIXES!!!
        for obstacle in self.obstacles:
            circle_collision = circle_line_segment_intersection(obstacle.coordinates, obstacle.radius,
                                                                self.character.position,
                                                                self.character.position + ray_vector, False)
            if len(circle_collision) > 0:
                pygame.draw.circle(window, (1, 24, 222), circle_collision[0], 5)
                end = (-circle_collision[0][0], -circle_collision[0][1])  # NEED FIX HERE
                target_pos = np.add(circle_collision[0],
                                    np.multiply(end, self.character.avoid_distance))
                self.target.position = target_pos
        return Seek.get_steering(self)


class ObstacleAvoidanceWander(Wander):
    collision_detector = Collision_Detector()
    obstacles = []

    def __init__(self, character, target, obstacles):
        super().__init__(character, target)
        self.obstacles = obstacles

    def get_steering(self):
        ray_vector = self.character.velocity
        ray_vector = normalize(ray_vector)
        ray_vector *= self.character.look_ahead
        pygame.draw.line(window, (255, 255, 255), self.character.position, self.character.position + ray_vector, 3)

        # Collision with walls
        collision = self.collision_detector.get_collision(self.character.position, ray_vector)
        if collision is not None:
            target_pos = np.add(collision.position,
                                np.multiply(collision.normal, self.character.avoid_distance))
            self.target = Static(target_pos, 0)
            return Seek.get_steering(self)

        # Collision with obstacles NEED FIXES
        for obstacle in self.obstacles:
            circle_collision = circle_line_segment_intersection(obstacle.coordinates, obstacle.radius,
                                                                self.character.position,
                                                                self.character.position + ray_vector, False)
            if len(circle_collision) > 0:
                pygame.draw.circle(window, (1, 24, 222), circle_collision[0], 5)
                end = (-circle_collision[0][0]-10, -circle_collision[0][1]-20)  # FIX HERE
                target_pos = np.add(circle_collision[0],
                                    np.multiply(end, self.character.avoid_distance))
                self.target = Static(target_pos, 0)
                return Seek.get_steering(self)
        return Wander.get_steering(self)


class CollisionAvoidance(ObstacleAvoidanceWander):
    max_acceleration = 2
    targets = []
    radius = 8

    def __init__(self, character, target, targets):

        super().__init__(character, target)
        self.targets = targets

    def get_steering(self):
        shortest_time = float('inf')
        first_target = None
        first_min_separation = -1
        first_relative_pos = None
        first_relative_vel = None
        steering = SteeringOutput()
        for target in self.targets:
            relative_pos = np.subtract(target.position, self.character.position)
            relative_vel = np.subtract(target.velocity, self.character.velocity)
            relative_speed = length(relative_vel)
            time_to_collision = np.divide(np.dot(relative_pos, relative_vel),
                                          np.multiply(relative_speed, relative_speed))
            distance = length(relative_pos)
            min_separation = np.subtract(distance, np.multiply(relative_speed, shortest_time))
            if min_separation > 2 * self.radius:
                continue
            if 0 < time_to_collision < shortest_time:
                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_relative_pos = relative_pos
                first_relative_vel = relative_vel
            if not first_target:
                break  # ObstacleAvoidanceWander.get_steering(self)
            if first_min_separation <= 0 or distance < 2 * self.radius:
                relative_pos = np.subtract(first_target.position, self.character.position)
            else:
                relative_pos = np.add(first_relative_pos, np.multiply(first_relative_vel, shortest_time))
            relative_pos = normalize(relative_pos)
            steering.linear = np.multiply(relative_pos, self.max_acceleration)
            return steering
        return ObstacleAvoidanceWander.get_steering(self)


class Zombie(Kinematic):
    steering = None
    target = None
    max_acceleration = 100
    radius = ZOMBIE_RADIUS
    other_zombies = []
    obstacles = []
    avoid_distance = 200
    look_ahead = 40

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
        elif option == "Separation_Wander":
            self.steering = Separation_Wander(self, self.other_zombies)
        elif option == "Align":
            self.steering = Align(self, self.target)
        elif option == "Obstacle_Avoidance":
            self.steering = ObstacleAvoidance(self, self.target, self.obstacles)
        elif option == "Obstacle_Avoidance_Wander":
            self.steering = ObstacleAvoidanceWander(self, self.target, self.obstacles)
        elif option == "Collision_Avoidance":
            self.steering = CollisionAvoidance(self, self.target, self.other_zombies)

    def run(self):
        self.update(self.steering.get_steering(), ZOMBIE_MAX_SPEED, ZOMBIE_TIME)
        self.draw()

    def draw(self):
        pygame.draw.circle(window, ZOMBIE_COLOR, self.position, ZOMBIE_RADIUS)

    def set_other_zombies(self):
        temp_zombies = []
        for zombie in self.other_zombies:
            if zombie is not self:
                temp_zombies.append(zombie)
        self.other_zombies = temp_zombies
