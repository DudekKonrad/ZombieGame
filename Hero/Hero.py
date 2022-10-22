from Variables.global_variables import *


class Hero:
    coordinates = [(0, 0), (0, 0), (0, 0)]
    size = [0, 0]
    speed = 0
    color = (0, 255, 0)

    def __init__(self, coordinates, size, speed):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed

    def hero_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.coordinates[1][0] > 0:
            self.step_left()
        if keys[pygame.K_RIGHT] and self.coordinates[2][0] < SCREEN_WIDTH:
            self.step_right()
        if keys[pygame.K_UP] and self.coordinates[0][1] > 0:
            self.step_up()
        if keys[pygame.K_DOWN] and self.coordinates[1][1] < SCREEN_HEIGHT:
            self.step_down()

    def draw_hero(self):
        self.hero_movement()
        window.fill((0, 0, 0))  # odswiezenie ekranu
        pygame.draw.polygon(window, self.color, self.coordinates, 0)

    def obstacle_collision(self):
        collide = pygame.Rect.colliderect(self.coordinates, Rect(200, 0, 50, 50))

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