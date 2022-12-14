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
    zombies.append(Zombie([random_x, random_y]))

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

    for z in zombies:
        if math.dist(z.position, Hero.get_position()) < ZOMBIE_CHASE_DISTANCE:
            z.set_target(Hero.get_position())
            z.set_steering("Obstacle_Avoidance")
        else:
            z.set_steering("Obstacle_Avoidance_Wander")
        z.run()

    pygame.display.update()
