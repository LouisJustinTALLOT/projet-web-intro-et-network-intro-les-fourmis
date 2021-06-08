

class Entity(object):
    def __init__(self, symbol):
        """
        Créé l'entité

        :param symbol: son symbole
        """
        self._x = None
        self._y = None
        self._symbol = symbol


class Player(Entity):
    def __init__(self, symbol="@"):
        """
        Créé le joueur

        :param symbol: son symbole
        """
        super().__init__(symbol)

    def move(self, dx, dy, map):
        """
        Déplace le joueur de dx et de dy.
        Change la carte sur le serveur python.

        :param dx: le déplacement en x
        :param dy: le déplacement en y
        :param map: la carte.
        :return: la requête à envoyer au joueur pour afficher le déplacement
        """
        new_x = self._x + dx
        new_y = self._y + dy

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = [{"i": f"{self._y}",
                     "j":f"{self._x}",
                     "content":"x"},
                    {"i": f"{new_y}",
                     "j":f"{new_x}",
                     "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        else:
            # n'a pas pu bouger
            ret = False
            data = []
        return data, ret