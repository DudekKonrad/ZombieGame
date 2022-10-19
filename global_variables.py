import pygame
from pygame.locals import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
hero_coordinates = [100, 100, 40, 40]  # (x, y, width, height)