import random

from game_backend.player import Entity


class Foe(Entity):
    
    def __init__(self, name, pt_life, strength, symbol, last_displacement=None):
        """
        Créé un nouveau monstre

        :param name: son nom.
        :param pt_life: ses points de vie.
        :param strength: sa force.
        :param symbol: son symbole affiché
        :param last_displacement: son dernier déplacement (None s'il vient d'apparaître)
        """
        self.last_displacement = last_displacement
        self.fight = False
        self.pt_life = pt_life
        self.strength = strength
        self.name = name
        self.last_was_x = False
        super().__init__(symbol)

    def move_foe(self, map):
        """
        Déplace le monstre.
        Change la carte sur le serveur python.

        :param map: la carte.
        :return: la requête à envoyer au joueur pour afficher le déplacement
        """
        this_was_x = False


        if not self.fight:
            moved = False
            vectors = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            if not self.last_displacement is None:
                vectors.remove((-self.last_displacement[0], -self.last_displacement[1]))
            random.shuffle(vectors)
            for vector in vectors:
                i, j = self._x + vector[0], self._y + vector[1]
                if map[j][i] in ['.', 'x']:
                    self.last_displacement = vector
                    self._x = i
                    self._y = j
                    moved = True

                    this_was_x = (map[j][i] == 'x')
                    break

            if not moved:
                return [], False

        to_replace = 'x' if self.last_was_x else '.'

        map[self._y][self._x] = self._symbol
        map[self._y - self.last_displacement[1]][self._x - self.last_displacement[0]] = to_replace


        data_foe = [{"i": f"{self._y}",
                    "j": f"{self._x}",
                         "content": self._symbol},
                        {"i": f"{self._y - self.last_displacement[1]}",
                         "j": f"{self._x - self.last_displacement[0]}",
                         "content": to_replace}]

        self.last_was_x = this_was_x

        return data_foe, True
    
    def __repr__(self):
        return self.name[0]