from .map_generator import Generator
from .entity import Player, Foe, Coin


class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._all_players = {}
        self._all_players[0] = Player(0)

        self._all_coins = []
        self._all_coins.append(Coin())

        self._all_foes = []
        self._all_foes.append(Foe('Dark Vador', 5, 25, 'D'))
        self._all_foes.append(Foe('Joker', 2, 25, "J"))

        for player in self._all_players.values():
            self.find_empty_pos(entity=player)

        for coin in self._all_coins:
            self.find_empty_pos(entity=coin)

        for foe in self._all_foes:
            self.find_empty_pos(entity=foe)

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

        packets = []

        for player in self._all_players.values():
            data_player, ret_player = player.move(dx, dy, self)
            packets.append( (data_player, ret_player) )

        for coin in self._all_coins:
            id_collected = coin.check_collected(self)
            if not id_collected == None:
                coin.kill_entity(self)
                self._all_players[id_collected].earn_money(coin._value)
                packets.append( ((self.build_data_earn(id_collected, coin._value)), True) )



        for foe in self._all_foes:
            if foe._alive:
                data_foe, ret_foe = foe.move_foe(self)
                packets.append( (data_foe, ret_foe))

        return packets

    def attack(self, player_id):
        player = self._all_players[player_id]

        for foe in self._all_foes:
            if foe._alive and foe.is_nearby(player):
                # on attaque ce monstre !
                data_fight = foe.attacked(self)
                return [data_fight,
                        (self.build_data_attack(foe.name, player_id, not foe._alive), True)]

        return [([], False)]

    def find_empty_pos(self, entity):
        """
        Trouve une position libre (ie un ".") sur la carte, puis l'ajoute à la carte.

        :param _map: la carte.
        :param entity: l'entité (un joueur, un monstre, etc.). Doit hériter de Entity
        """
        n_row = len(self._map)
        # n_col = len(self._map[0])

        y_init = n_row // 2
        found = False
        while found is False:
            y_init += 1
            for i, c in enumerate(self._map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        entity._x = x_init
        entity._y = y_init

        self._map[entity._y][entity._x] = entity._symbol

    def build_data_displacement(self, new_x, new_y, new_content, old_x, old_y, old_content):
        return [{"descr": "displacement",
                 "i": f"{old_y}",
                 "j": f"{old_x}",
                 "content": old_content},
                {"descr": "displacement",
                 "i": f"{new_y}",
                 "j": f"{new_x}",
                 "content": new_content}]

    def build_data_earn(self, player_id, earned_amount):
        return [{"descr": "earn",
                 "ident": f"{player_id}",
                 "val": f"{earned_amount}"},
                {"foo": "bar"}]

    def build_data_attack(self, foe_name, player_id, is_dead):
        return [{"descr": "fight",
                 "ident": f"{player_id}",
                 "target": f"{foe_name}",
                 "isdead": f"{is_dead}"},
                {"foo": "bar"}]