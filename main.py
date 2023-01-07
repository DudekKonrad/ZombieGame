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

for z in zombies:
    z.set_obstacle_left_value() #tu ustawiam randomowe wartosci zeby kazdy obiekt zombiaka mial inny prog opuszczania przxeszkody

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((0, 0, 0))
    Hero.draw_hero()
    Hero.hero_input()
    Map.draw_map()

    pom = 0
    for z in zombies:
        # z.set_obstacle_left_value()
        pom = Map.get_nearest_obstacle(z.position)
        print(z.count_nearby_zombies(20))
        if pom > -1 and z.count_nearby_zombies(20) < 3:
            if z.time_counter > z.how_long_zombie_will_stay_behind_obstacle: #jezeli dany zombiak bedzie przy przeeszkodzie ale minie okreslona ilosc czasu to wejdzie do tego ifa i zacznie suzkac innej przeszkody
                pom2 = pom
                pom = Map.get_nearest_obstacle_but_ignoring_one(z.position, pom2) #szukanie przeszkody innej niz ta przy ktorej przed chwila bylem
                z.change_to_left_obstacle_color() #fioletowy kolor mowi o tym ze szukam innej przeszkody, zielony ze regularny zombiak a czerwony ze atakuje (tutaj bedzie fioletowy)
            else:
                z.set_target(get_hide_coordinates(Hero.get_position(), Map.get_obstacle_position(pom)))
                z.set_steering("Obstacle_Avoidance")
                z.time_counter = z.time_counter + 1 #inkrementuje counter w momencie gdy sie chowam za przeszkoda
        elif z.count_nearby_zombies(20) >= 3:
            z.change_to_attack_color()
            z.set_target(Hero.get_position())
            z.set_steering("Obstacle_Avoidance")
        else:
            z.time_counter = 0
            z.set_steering("Separation")
        z.run()
    print(" ")

    pygame.display.update()
