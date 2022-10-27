import pygame


class Obstacle:
    coordinates = [0, 0]
    radius = 0
    color = (100, 100, 100)

    def __init__(self, coordinates, radius):
        self.coordinates = coordinates
        self.radius = radius

    def draw_obstacle(self, screen):
        pygame.draw.circle(screen, self.color, self.coordinates, self.radius)
