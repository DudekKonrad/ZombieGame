from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Map = Map(window)
Map.make_map()
zombies = []

for i in range(NUMBER_OF_ENEMIES):
    random_x = random.randint(FRAME_SIZE, SCREEN_WIDTH - FRAME_SIZE)
    random_y = random.randint(FRAME_SIZE, SCREEN_HEIGHT - FRAME_SIZE)
    zombie_to_add = Zombie(Vector2(random_x, random_y))
    zombies.append(zombie_to_add)

Map.enemies = zombies
Hero = Hero(HERO_START_POSITION, HERO_SPEED, Map)

# Initialize zombies
for z in zombies:
    z.other_zombies = zombies
    z.set_other_zombies()
    z.set_obstacles(Map.obstacles)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((0, 0, 0))
    Hero.draw_hero()
    Map.draw_map()
    Hero.hero_input()

    # for z in zombies:
    #     if math.dist(z.position, Hero.get_position()) < ZOMBIE_CHASE_DISTANCE:
    #         z.set_target(Hero.get_position())
    #         z.set_steering("Obstacle_Avoidance")
    #     else:
    #         z.set_steering("Obstacle_Avoidance_Wander")
    #     z.run()

    # print("hero = ", Hero.get_position())
    
    # get_hide_coordinates(Hero.get_position(), Map.get_obstacle_position(0))
    pom = 0
    for z in zombies:
        pom = Map.get_nearest_obstacle(z.position)
        if pom > -1 and z.count_nearby_zombies(20) < 4:
            print(pom)
            print(Map.get_obstacle_position(pom))
            z.set_target(get_hide_coordinates(Hero.get_position(), Map.get_obstacle_position(pom)))
            z.set_steering("Obstacle_Avoidance")
        elif z.count_nearby_zombies(20) >= 4:
            z.set_target(Hero.get_position())
            z.set_steering("Obstacle_Avoidance")
        else:
            z.set_steering("Separation")
            
        z.run()

    pygame.display.update()
