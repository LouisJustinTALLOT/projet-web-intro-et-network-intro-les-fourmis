import random


class Foe():
    
    def __init__(self, name, position, pt_life, strength, last_displacement=None) :
        self.position = position
        self.last_displacement = last_displacement
        self.fight = False
        self.pt_life = pt_life
        self.strength = strength
        self.name = name

    def move(self, donjon):
        if not self.fight:
            vectors = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            if not self.last_displacement == None:
                vectors.remove((-self.last_displacement[0], -self.last_displacement[1]))
            random.shuffle(vectors)
            for vector in vectors:
                i, j = self.position[0] + vector[0], self.position[1] + vector[1]
                if donjon.matrix[i][j].obstacle.env_type in ['floor', 'corridor', 'door']:
                    self.last_displacement = vector
                    self.position = (i, j)
                    break
    
    def __repr__(self):
        return self.name[0]
        



    








