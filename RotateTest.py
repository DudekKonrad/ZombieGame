import pygame
from math import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Triangle:
    points = [(400, 500), (600, 500), (500, 200)]
    old_angle = 0

    def get_angle(self, destination):
        x_dist = destination[0] - self.get_center()[0]
        y_dist = destination[1] - self.get_center()[1]
        return atan2(-y_dist, x_dist) % (2 * pi)

    def angle2(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = self.points[2][0], self.points[2][1]

        dir_x, dir_y = mouse_x - player_x, mouse_y - player_y

        # self.rot = (180 / math.pi) * math.atan2(-dir_y, dir_x)
        # self.rot = (180 / math.pi) * math.atan2(-dir_y, dir_x) - 45
        return (180 / pi) * atan2(-dir_x, -dir_y)

    def get_center(self):
        n = len(self.points)
        cx = sum(p[0] for p in self.points) / n
        cy = sum(p[1] for p in self.points) / n
        return cx, cy

    def rotate(self, angle):
        new_points = []
        #if self.old_angle == angle:
        #return
        for p in self.points:
            tx, ty = p[0] - self.get_center()[0], p[1] - self.get_center()[1]
            new_x = (tx * cos(angle) - ty * sin(angle)) + self.get_center()[0]
            new_y = (tx * sin(angle) + ty * cos(angle)) + self.get_center()[1]
            new_points.append((new_x, new_y))
        #self.old_angle = angle
        self.points = new_points


pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

triangle = Triangle()
triangle2 = Triangle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - triangle.get_center()[0], mouse_y - triangle.get_center()[1]
    angle = -atan2(rel_y, rel_x)
    if pygame.key.get_pressed()[pygame.K_s]:
        triangle2.rotate(radians(180))
    triangle.rotate(triangle.angle2())
    window.fill((0, 0, 0))
    pygame.draw.polygon(window, (255, 0, 0), triangle.points, 0)
    pygame.draw.polygon(window, (0, 255, 0), triangle2.points, 0)
    pygame.draw.circle(window, (0, 0, 255), (triangle.get_center()[0], triangle.get_center()[1]), 10)
    pygame.display.update()
