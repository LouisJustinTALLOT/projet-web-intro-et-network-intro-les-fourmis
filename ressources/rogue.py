import pygame as pg
import random
from interface import Interface
from hero import Hero
from donjon import Donjon, Room, Obstacle, Box

foodimg = pg.image.load('food.png')


n_x = 15
n_y = 20
width = 20

pg.init()
screen = pg.display.set_mode((n_x*width, n_y*width))
clock = pg.time.Clock()

interface = Interface(width, screen)

# on rajoute une condition à la boucle: si on la passe à False le programme s'arrête
running = True
hero = Hero((5, 5))

my_donjon = Donjon(n_x, n_y)
room1 = Room(1, 5, 2, 6, [(2, 2), (5, 5)])
room2 = Room(3, 9, 9, 13, [(4, 9), (8, 13)])
room3 = Room(7, 13, 15, 18, [(8, 15)], [(12, 17)])
my_donjon.new_room(room1)
my_donjon.new_room(room2)
my_donjon.new_room(room3)
my_donjon.new_corridor(room1, room2)
my_donjon.new_corridor(room2, room3)
my_donjon.add_items()
my_donjon.add_foes()
"""
for i in range(n_x) :
    for j in range(n_y) :
        interface.display(i, j, my_donjon.matrix[i][j].obstacle.env_type)
"""

x, y = hero.position

count = 0 

while running:
    clock.tick(10)

    # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
    # ici donc tous les évènements survenus durant la seconde précédente


    for event in pg.event.get():
        # chaque évênement à un type qui décrit la nature de l'évênement
        # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
        if event.type == pg.QUIT:
            running = False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:

            #Déplacement
            if event.key == pg.K_UP:
                v = (0, -1)
                hero.move(my_donjon, v)
            
            if event.key == pg.K_DOWN:
                v = (0, 1)
                hero.move(my_donjon, v)
            
            if event.key == pg.K_RIGHT:
                v = (1, 0)
                hero.move(my_donjon, v)
            
            if event.key == pg.K_LEFT:
                v = (-1, 0)
                hero.move(my_donjon, v)
            
            #Action
            if event.key == pg.K_SPACE:
                hero.use("right")

            if event.key == pg.K_LSHIFT:
                hero.use("left")

            #Parcours de l'inventaire
            """
            if event.key == pg.K_q:
                interface.switch_left_hand = (interface.switch_left_hand + 1) % 2
            """
            if event.key == pg.K_d:
                hero.switch_inventory("left")
                interface.event(hero)

            if event.key == pg.K_q:
                hero.switch_inventory("right")
                interface.event(hero)

            if event.key == pg.K_s:
                interface.print_inventory(hero)
    
    current_room = my_donjon.matrix[x][y].in_room

    interface.display(x, y, my_donjon)

    x, y = hero.position

    if current_room :
        for i in range(current_room.x_min, current_room.x_max + 1) :
            for j in range(current_room.y_min, current_room.y_max + 1) :
                interface.display(i, j, my_donjon)
    else :
        interface.display(x, y, my_donjon)


    for foe in my_donjon.foes :
        x0, y0 = foe.position
        if not count % 10 :
            foe.move(my_donjon)
        if my_donjon.matrix[foe.position].in_room == current_room :
            print("ergerg")
            interface.display(x0, y0, my_donjon)
            pg.draw.circle(screen, (255, 0, 0), ((x0+0.5)*width, (y0+0.5)*width), width*0.5)

    pg.draw.circle(screen, (0, 255, 0), ((x+0.5)*width, (y+0.5)*width), width*0.3)



    pg.display.update()

    count += 1

# Enfin on rajoute un appel à pg.quit()
# Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
pg.quit()