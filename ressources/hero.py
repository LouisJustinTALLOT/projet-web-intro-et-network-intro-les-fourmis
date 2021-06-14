import pygame as pg
from donjon import *
from item import Item
from foe import Foe


class Hero: 

    def __init__(self, init_pos: tuple):
        self.position = init_pos
        self.coins = 0
        self.pt_life = 20
        self.pt_stamina = 20
        self.head = None
        self.chest = None
        self.right_hand = None
        self.left_hand = None
        self.feet = None
        self.back_pack = {'weapon': [], 'food': [], 'potion': []}
        self.inventory = []   #on enregistre les objets de type weapon...


    def collect(self, donjon):
        i, j = self.position[0], self.position[1]
        element = donjon.matrix[i][j].item
        if element :
            if element.nature == 'gold':
                self.coins += element.value
            elif element.nature == 'weapon':
                self.back_pack['weapon'].append(element)     #on ajoute les éléments trouvés dans le back_pack et dans le inventory
                self.inventory.append(element)
            elif element.nature == 'food':
                self.back_pack['food'].append(element)
                self.inventory.append(element) 
            elif element.nature == 'potion':
                self.back_pack['potion'].append(element)
                self.inventory.append(element)
            donjon.matrix[i][j].item = None    

    def move(self, donjon, vector):

        """
        deplace le hero si le mouvement est permis 
        """

        i, j = self.position[0] + vector[0], self.position[1] + vector[1]
        if donjon.matrix[i][j].obstacle.env_type in ['floor', 'corridor', 'door']:
            self.position = (i, j)
            self.collect(donjon)
        elif donjon.matrix[i][j].obstacle.env_type == 'wall':
            return 'only spirits can cross walls...'
        elif donjon.matrix[i][j].obstacle.env_type == 'stairs':
            return 'well done !'
        

    def switch_inventory(self, hand):   
        if len(self.inventory) == 0:
            return "collect some objects !" 
        elif hand == 'right':
            if self.right_hand == None:
                self.right_hand = self.inventory.pop()
            else:
                self.inventory = self.right_hand + self.inventory
                self.right_hand = self.inventory.pop()
        
        elif hand == 'left':
            if self.left_hand == None:
                self.left_hand = self.inventory.pop()
            else:
                self.inventory = self.left_hand + self.inventory
                self.left_hand = self.inventory.pop()
            
    def use_item(self, item):
        if item.nature == 'food':
            self.pt_stamina += item.amount
        elif item.nature == 'potion':
            self.pt_life += item.amount
        

    def use(self, hand):
        if hand == 'right':
            if self.right_hand == None:
                return 'take an item with your right hand'
            else:
                self.use_item(self.right_hand)
        elif hand == 'left':
            if self.left_hand == None:
                return 'take an item with your left hand'
            else:
                self.use_item(self.left_hand)
            
            
def strike_possible(hero, foe):
        i_h, j_h = hero.position[0], hero.position[1]
        i_f, j_f = foe.position[0], foe.position[0]
        if abs(i_h - i_f) <= 1 and abs(j_h - j_f) <= 1:
            foe.fight = True    

#def strike(hero, foe): 

            




        






        
