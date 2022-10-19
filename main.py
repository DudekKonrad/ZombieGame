from map import *
from hero import *

pygame.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_hero()
    draw_map()
    pygame.display.update()