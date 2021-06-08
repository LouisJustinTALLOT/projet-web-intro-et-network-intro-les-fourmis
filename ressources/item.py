#appels possibles pour créer un objet : 
#Item('gold', 10)
#Item('weapon', 'sword') #arme et type d'arme
#Item('food', 10) #santé

class Item():
    def __init__(self, nature):
        self.nature = nature


class Gold(Item):

    def __init__(self, nature, value):
        super().__init__(nature)
        self.value = value
    
    def __repr__(self):
        return '$'


class Food(Item):

    def __init__(self, nature, amount):
        super().__init__(nature)
        self.amount = amount
    
    def __repr__(self):
        return '&'

class Weapon(Item):

    def __init__(self, nature, category: 'str'):
        super().__init__(nature)
        self.category = category
    
    def __repr__(self):
        return '!'

class Potion(Item):

    def __init__(self, nature, amount):
        super().__init__(nature)
        self.amount = amount
    
    def __repr__(self):
        return 'j'