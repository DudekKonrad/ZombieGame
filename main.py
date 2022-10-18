import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
hero_coordinates = [100, 100, 40, 40]  # (x, y, width, height)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_map():
    # TODO dodac collidery + dobrze podobno zeby przeszkody
    # ukladaly sie za kazdym uruchomieniem inaczej
    pygame.draw.circle(window, (100, 100, 100), [300, 200], 60, 0)
    pygame.draw.circle(window, (100, 100, 100), [800, 600], 70, 0)
    pygame.draw.circle(window, (100, 100, 100), [750, 200], 40, 0)
    pygame.draw.circle(window, (100, 100, 100), [200, 590], 50, 0)

    pygame.draw.rect(window, (100, 100, 100), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)


def hero_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and hero_coordinates[0] > 0:
        hero_coordinates[0] -= 0.5
    if keys[pygame.K_RIGHT] and hero_coordinates[0] < SCREEN_WIDTH:
        hero_coordinates[0] += 0.5
    if keys[pygame.K_UP] and hero_coordinates[1] > 0:
        hero_coordinates[1] -= 0.5
    if keys[pygame.K_DOWN] and hero_coordinates[1] < SCREEN_HEIGHT:
        hero_coordinates[1] += 0.5


def draw_hero():
    hero_movement()
    window.fill((0, 0, 0))  # odswiezenie ekranu
    pygame.draw.rect(window, (255, 0, 0), hero_coordinates, 0)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_hero()
    draw_map()
    pygame.display.update()