from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Hero = Hero(HERO_START_POSITION, HERO_SIZE, HERO_SPEED)
Map = Map(window)
Map.make_map()
zombie = Zombie()
#radius, position, time, orientation, velocity, rotation, steering.linear, steering.angular

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # time.sleep(0.05)
    Hero.draw_hero()
    Hero.calculate_angle(pygame.mouse.get_pos())
    Map.draw_map()
    for obstacle in Map.obstacles:
        Hero.check_if_collide(obstacle)
    # zombie.kinematic_update()
    # zombie.kinematic_arrive(Hero.get_center())
    # zombie.wandering()
    # zombie.collision_avoidance(Map.obstacles)
    # zombie.update(Hero.get_center())
    zombie.draw()
    zombie.update(Hero.get_center())
    pygame.display.update()
