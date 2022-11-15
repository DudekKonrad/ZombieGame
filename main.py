from Map import *
from Hero.Hero import *
from Variables.hero_variables import *
from Zombie.Zombie import *

pygame.init()

Map = Map(window)
Map.make_map()
# zombies = [Zombie([503.0, 400.0]), Zombie([500.0, 400.0]), Zombie([506.0, 400.0])]
zombies = []
for i in range(NUMBER_OF_ENEMIES):
    random_x = random.randint(FRAME_SIZE, SCREEN_WIDTH - FRAME_SIZE)
    random_y = random.randint(FRAME_SIZE, SCREEN_HEIGHT - FRAME_SIZE)
    zombies.append(Zombie([random_x, random_y]))

Map.enemies = zombies
Hero = Hero(HERO_START_POSITION, HERO_SPEED, Map)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Hero.draw_hero()
    Map.draw_map()
    Hero.hero_input()

    for zombie in zombies:
        zombie.set_other_zombies(zombies[:])
        zombie.draw()
        zombie.update()
    print("-----------------")

    pygame.display.update()
