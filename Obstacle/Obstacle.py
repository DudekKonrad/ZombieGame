import pygame


class Obstacle:
    x = 0
    y = 0
    radius = 0
    color = (100, 100, 100)

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


    def draw_obstacle(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
