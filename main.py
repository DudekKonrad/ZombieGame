from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Hero = Hero(HERO_START_POSITION, HERO_SIZE, HERO_SPEED)
Map = Map(window)
Map.make_map()
zombie = Zombie()
# zombie2 = Zombie([100.0, 200.0])
#radius, position, time, orientation, velocity, rotation, steering.linear, steering.angular

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # time.sleep(0.5)
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
    # print("zombie1 = ", zombie.wander.character.position)
    # print("zombie2 = ", zombie2.wander.character.position)
    
    zombie.draw()
    # zombie2.draw()
    # print("")
    # zombie.update(3.14) #testData
    # zombie.update([1.0, 2.2])
    zombie.update()
    # zombie2.update()
    pygame.display.update()
