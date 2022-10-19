from global_variables import *

def draw_map():
    # TODO dodac collidery + dobrze podobno zeby przeszkody
    # ukladaly sie za kazdym uruchomieniem inaczej
    pygame.draw.circle(window, (100, 100, 100), [300, 200], 60, 0)
    pygame.draw.circle(window, (100, 100, 100), [800, 600], 70, 0)
    pygame.draw.circle(window, (100, 100, 100), [750, 200], 40, 0)
    pygame.draw.circle(window, (100, 100, 100), [200, 590], 50, 0)

    pygame.draw.rect(window, (100, 100, 100), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)

