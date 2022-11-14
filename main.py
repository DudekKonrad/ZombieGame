from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Map = Map(window)
Map.make_map()
zombies = [Zombie([500.0, 500.0]), Zombie([660.0, 600.0]), Zombie([860.0, 600.0])]
Map.enemies = zombies
Hero = Hero(HERO_START_POSITION, HERO_SPEED, Map)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # time.sleep(0.5)
    window.fill((0, 0, 0))  # odswiezenie ekranu
    Hero.draw_hero()
    Hero.calculate_angle(pygame.mouse.get_pos())
    Map.draw_map()
    Hero.hero_input()

    for zombie in zombies:
        zombie.draw()
        zombie.update()

    pygame.display.update()
