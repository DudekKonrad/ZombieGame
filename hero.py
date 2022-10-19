from global_variables import *

#tu moze zrobic klase "Hero" i do niej 
# wrzucic hero_coordinates z global_variables.py????

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
