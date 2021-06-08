#appels possibles pour créer un objet : 
#Object('gold', 10)
#Object('weapon', 'sword') #arme et type d'arme
#Object('food', 10) #santé

class Object():
    def __init__(self, nature):
        self.nature = nature

class Gold(Object):
    def __init__(self, nature, value):
        super().__init__(nature)
        self.value = value

class Food(Object):
    def __init__(self, nature, amount):
        super().__init__(nature)
        self.amount = amount

class Weapon(Object):
    def __init__(self, nature category: 'str'):
        super().__init__(nature)
        self.category = category