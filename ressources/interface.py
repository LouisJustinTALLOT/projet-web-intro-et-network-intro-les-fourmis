import pygame as pg
from donjon import Donjon
from item import Item, Gold, Weapon, Potion, Food
from hero import Hero


class Interface :

    def __init__(self, width, screen) :
        self.switch_left_hand = 0
        self.width = width
        self.screen = screen

    def display(self, x, y, donjon) :
        env_type = donjon.matrix[x, y].obstacle.env_type
        item = donjon.matrix[x, y].item
        if env_type == "wall" :
            rect = pg.Rect((x)*self.width, (y)*self.width, self.width, self.width)
            pg.draw.rect(self.screen, (255, 255, 255), rect)
        
        if env_type == "corridor" :
            rect = pg.Rect((x)*self.width, (y)*self.width, self.width, self.width)
            pg.draw.rect(self.screen, (100, 100, 100), rect)
   
        if env_type == "door" :
            rect = pg.Rect((x)*self.width, (y)*self.width, self.width, self.width)
            pg.draw.rect(self.screen, (50, 50, 50), rect)

        if env_type == "stairs" :
            rect = pg.Rect((x)*self.width, (y)*self.width, self.width, self.width)
            pg.draw.rect(self.screen, (0, 0, 255), rect)

        if env_type == "floor" :
            rect = pg.Rect((x)*self.width, (y)*self.width, self.width, self.width)
            pg.draw.rect(self.screen, (0, 0, 0), rect)

        if isinstance(item, Gold) :
            rect = pg.Rect((x+0.25)*self.width, (y+0.25)*self.width, self.width*0.5, self.width*0.5)
            pg.draw.rect(self.screen, (255, 0, 255), rect)

        if isinstance(item, Food) :
            rect = pg.Rect((x+0.25)*self.width, (y+0.25)*self.width, self.width*0.5, self.width*0.5)
            pg.draw.rect(self.screen, (255, 100, 100), rect)  

        if isinstance(item, Weapon) :
            rect = pg.Rect((x+0.25)*self.width, (y+0.25)*self.width, self.width*0.5, self.width*0.5)
            pg.draw.rect(self.screen, (0, 0, 255), rect)

        if isinstance(item, Potion) :
            rect = pg.Rect((x+0.25)*self.width, (y+0.25)*self.width, self.width*0.5, self.width*0.5)
            pg.draw.rect(self.screen, (0, 255, 0), rect)          
        

    def event(self, hero, item=None ) :
        if item.nature == "gold" :
            print(f"Bourse de {item.value}")
        
        if item.nature == "food":
            print(f"Nourriture de {item.amount} calories")

        if item.nature == "weapon":
            print(f"Arme de type {item.category}")

        if typ == "or" :
            print(f"Bourse de ")

        print(f"Points de vie : {hero.pt_life}")
        if self.switch_left_hand :
            print(f" - Main gauche : {hero.left_hand}")
            print(f"Main droite : {hero.right_hand}")
        else :
            print(f" - Main droite : {hero.left_hand}")
            print(f"Main gauche : {hero.right_hand}")

    def print_inventory(self, hero: Hero):
        for item in hero.inventory:
            print(item)
