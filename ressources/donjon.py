import numpy as np
import random
from item import *
from foe import *

#taille de la matrice donjon
width = 20
height = 15

types_set = {'wall', 'corridor', 'stairs', 'door', 'floor', 'void'}

class Donjon():

    def __init__(self, height, width):
        #self.matrix est une matrice de cases
        self.matrix = np.empty((height, width), dtype=Box)
        for i in range(height):
            for j in range(width):
                self.matrix[i][j] = Box(Obstacle('void'))
        self.rooms = []

    def new_room(self, room):
        """
            x_min, ..., y_max les extrémités de la salle, 
            doors la liste des portes (leurs coordonnées dans la matrice),
            stairs la liste des escaliers (leurs coordonnées dans la matrice)
        """
        #création des murs et du sol de la salle
        for i in range(room.x_min, room.x_max + 1):
            for j in range(room.y_min, room.y_max + 1):
                self.matrix[i][j].in_room = room
                if i in {room.x_min, room.x_max} or j in {room.y_min, room.y_max}:
                    self.matrix[i][j].obstacle.env_type = 'wall'
                else:
                    self.matrix[i][j].obstacle.env_type = 'floor'
        
        #création des portes de la salle
        for i, j in room.doors:
            self.matrix[i][j].obstacle.env_type = 'door'
        
        #création des escaliers de la salle
        for i, j in room.stairs:
            self.matrix[i][j].obstacle.env_type = 'stairs'
        
        self.rooms.append(room)

    def new_corridor(self, room1, room2):
        """
            génère aléatoirement un couloir entre les salles 1 et 2
        """
        #choix aléatoire de portes dans chaque salle (tuple des coordonnées)
        door1 = random.choice(room1.doors)
        door2 = random.choice(room2.doors)

        path = set()
        founded = False
        current_box = door1
        cases_parcourues = 0

        while not founded:
            #on construit une liste des directions ordonné par intérêt (va dans la direction globale souhaitée)
            if abs(door2[0] - current_box[0]) < abs(door2[1] - current_box[1]):
                if (door2[1] - current_box[1] > 0) and (door2[0] - current_box[0] > 0):
                    prioritary_directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                elif (door2[1] - current_box[1] > 0) and (door2[0] - current_box[0] <= 0):
                    prioritary_directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]
                elif (door2[1] - current_box[1] <= 0) and (door2[0] - current_box[0] > 0):
                    prioritary_directions = [(0, -1), (1, 0), (-1, 0), (0, 1)]
                elif (door2[1] - current_box[1] <= 0) and (door2[0] - current_box[0] <= 0):
                    prioritary_directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
            else:
                if (door2[1] - current_box[1] > 0) and (door2[0] - current_box[0] > 0):
                    prioritary_directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
                elif (door2[1] - current_box[1] > 0) and (door2[0] - current_box[0] <= 0):
                    prioritary_directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
                elif (door2[1] - current_box[1] <= 0) and (door2[0] - current_box[0] > 0):
                    prioritary_directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]
                elif (door2[1] - current_box[1] <= 0) and (door2[0] - current_box[0] <= 0):
                    prioritary_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

            #on parcours les directions possibles en avançant seulement si l'on tombe sur du vide ou un couloir
            for di, dj in prioritary_directions:
                i, j = current_box
                if (i + di, j + dj) == door2:
                    path.add((i + di, j + dj))
                    founded = True
                    break
                elif (0 <= i + di < height) and (0 <= j + dj < width) and not ((i + di, j + dj) in path):
                    if self.matrix[i + di][j + dj].obstacle.env_type in  {'void', 'corridor'}:
                        self.matrix[i + di][j + dj].obstacle.env_type = 'corridor'
                        current_box = (i + di, j + dj)
                        path.add((i + di, j + dj))
                        break        

    def new_corridor_dumb(self, boxs_list):
        for i, j in boxs_list:
            self.matrix[i][j].obstacle.env_type = 'corridor'
    
    def add_items(self):
        sword = Weapon('weapon', 'sword')
        gold = Gold('gold', 10)
        food = Food('food', 10)
        potion = Potion('potion', 10)
        items = {sword, gold, food, potion}

        for item in items:
            room = random.choice(self.rooms)
            while True:
                i = random.randint(room.x_min + 1, room.x_max - 1)
                j = random.randint(room.y_min + 1, room.y_max - 1)
                #on vérifie qu'il n'y a pas déjà d'objet sur la case
                if not self.matrix[i][j].item:
                    self.matrix[i][j].item = item
                    break
    
    def add_foes(self):
        dark_vador = Foe('Dark Vador', None, 50, 25)
        voldemord = Foe('Voldemord', None, 10, 30)
        golum = Foe('Golum', None, 10, 2)
        self.foes = {dark_vador, voldemord, golum}

        for my_foe in self.foes:
            room = random.choice(self.rooms)
            while True:
                i = random.randint(room.x_min + 1, room.x_max - 1)
                j = random.randint(room.y_min + 1, room.y_max - 1)
                #on vérifie qu'il n'y a pas déjà d'objet sur la case
                if not self.matrix[i][j].foe:
                    my_foe.position = (i, j)
                    self.matrix[i][j].foe = my_foe
                    break
    
    def __repr__(self):
        return repr(self.matrix)

class Obstacle():

    def __init__(self, env_type):
        self.env_type = env_type

    def __repr__(self):
        if self.env_type == 'wall':
            return '-'
        elif self.env_type == 'corridor':
            return '#'
        elif self.env_type == 'stairs':
            return '='
        elif self.env_type == 'door':
            return '+'
        elif self.env_type == 'floor':
            return '.'
        elif self.env_type == 'void':
            return ' '
        else:
            return ' '

class Box():

    def __init__(self, obstacle, item=None, foe=None):
        self.obstacle = obstacle
        self.item = item
        self.foe = foe
        self.in_room = None
    
    def __repr__(self):
        if self.foe:
            return repr(self.foe)
        if self.item:
            return repr(self.item)
        else:
            return repr(self.obstacle)

class Room():

    def __init__(self, x_min, x_max, y_min, y_max, doors=[], stairs=[]):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.doors = doors
        self.stairs = stairs

my_donjon = Donjon(height, width)
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
print(my_donjon)

