from Map import *
from Hero.Hero import *
from Variables.hero_variables import *

pygame.init()

Hero = Hero(HERO_START_POSITION, HERO_SIZE, HERO_SPEED)
Map = Map(window)
Map.make_map()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Hero.draw_hero()
    Map.draw_map()
    pygame.display.update()
