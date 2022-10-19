from Variables.global_variables import *


class Hero:
    coordinates = [0, 0]
    size = [0, 0]
    speed = 0
    color = (0, 255, 0)

    def __init__(self, coordinates, size, speed):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed

    def hero_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.coordinates[0] > 0:
            self.coordinates[0] -= self.speed
        if keys[pygame.K_RIGHT] and self.coordinates[0] < SCREEN_WIDTH:
            self.coordinates[0] += self.speed
        if keys[pygame.K_UP] and self.coordinates[1] > 0:
            self.coordinates[1] -= self.speed
        if keys[pygame.K_DOWN] and self.coordinates[1] < SCREEN_HEIGHT:
            self.coordinates[1] += self.speed

    def draw_hero(self):
        self.hero_movement()
        window.fill((0, 0, 0))  # odswiezenie ekranu
        pygame.draw.rect(window, self.color, [self.coordinates, self.size], 0)
