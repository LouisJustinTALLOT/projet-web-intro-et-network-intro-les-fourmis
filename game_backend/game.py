from .foe import Foe
from .map_generator import Generator
from .player import Player


class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._player = Player()
        self._foe = Foe('Dark Vador', 50, 25, 'D')
        # self._player.initPos( self._map )
        self.find_empty_pos(self._map, entity=self._player)
        self.find_empty_pos(self._map, entity=self._foe)

    def getMap(self):
        return self._map

    def move_all(self, dx, dy):
        """
        Bouge le joueur de dx et de dy, ainsi que les monstres.
        Modifie les positions sur la carte.

        :param dx: déplacement en x du joueur
        :param dy: déplacement en y du joueur
        :return: les requêtes à envoyer au joueur
         (dans l'ordre, data_player (pour l'affichage du joueur),
                        ret_player (si oui ou non le joueur a bougé),
                        data_foe (pour l'affichage du monstre) et
                        ret_foe (si oui ou non le monstre a bougé))
        """
        data_player, ret_player =  self._player.move(dx, dy, self._map)
        data_foe, ret_foe = self._foe.move_foe(self._map)

        return data_player, ret_player, data_foe, ret_foe

    def find_empty_pos(self, _map, entity):
        """
        Trouve une position libre (ie un ".") sur la carte, puis l'ajoute à la carte.

        :param _map: la carte.
        :param entity: l'entité (un joueur, un monstre, etc.). Doit hériter de Entity
        """
        n_row = len(_map)
        # n_col = len(_map[0])

        y_init = n_row // 2
        found = False
        while found is False:
            y_init += 1
            for i, c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        entity._x = x_init
        entity._y = y_init

        _map[entity._y][entity._x] = entity._symbol