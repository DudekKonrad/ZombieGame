from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Hero = Hero(HERO_START_POSITION, HERO_SIZE, HERO_SPEED)
Map = Map(window)
Map.make_map()
zombie = Zombie(15, [300.0, 300.0], 0.02, 0.0, [0.05, 0.0], 0.0, [0.0, 0.0], 0.0)
#radius, position, time, orientation, velocity, rotation, steering.linear, steering.angular

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # time.sleep(0.5)
    Hero.draw_hero()
    Map.draw_map()
    zombie.kinematic_update()
    zombie.kinematic_seek()

    zombie.draw()
    pygame.display.update()
