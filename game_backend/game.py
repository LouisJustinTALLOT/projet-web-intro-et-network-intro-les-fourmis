from random import random, randrange
from typing import Dict

from .map_generator import Generator
from .entity import NextLevel, Player, Foe, Coin


class Game:
    def __init__(self, width=76, height=32):
        self._w = width
        self._h = height
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._all_players: Dict[int, Player] = {} 
        self._nb_players = -1

        self._current_level = 1

        self._all_coins = []
        self._all_foes = []
        self._next_level = NextLevel()

        self._all_coins.append(Coin())
        self._all_coins.append(Coin())
        self._all_foes.append(Foe('Dark Vador', 4, 10, 'DV'))
        self._all_foes.append(Foe('Joker', 2, 7, "Jo"))
        self._all_coins.append(Coin())
        self._all_coins.append(Coin())
        self._all_foes.append(Foe('Voldemord', 5, 12, 'Vd'))
        self._all_foes.append(Foe('Gollum', 1, 4, "Go"))
        self._all_coins.append(Coin())
        self._all_coins.append(Coin())

        for player in self._all_players.values():
            self.find_empty_pos(entity=player)

        for coin in self._all_coins:
            self.find_empty_pos(entity=coin)

        for foe in self._all_foes:
            self.find_empty_pos(entity=foe)

        self.find_empty_pos(entity=self._next_level) 

        self._dict_level_genere = {1: True}

    def add_new_player(self):
        symbol = "@0"
        new_player = Player(self._nb_players + 1, symbol)
        self._all_players[self._nb_players + 1] = new_player
        self.find_empty_pos(entity = new_player)
        self._nb_players += 1
        return self._nb_players

    def getMap(self):
        return self._map

    def new_map(self):
        self._generator = Generator(width=self._w, height=self._h)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level
        
        self._all_coins = []
        self._all_foes = []
        self._next_level = NextLevel()

        self._all_coins.append(Coin())
        self._all_coins.append(Coin())
        self._all_foes.append(Foe('Dark Vador', 4, 10, 'DV'))
        self._all_foes.append(Foe('Joker', 2, 7, "Jo"))
        self._all_coins.append(Coin())
        self._all_coins.append(Coin())
        self._all_foes.append(Foe('Voldemord', 5, 12, 'Vd'))
        self._all_foes.append(Foe('Gollum', 1, 4, "Go"))
        self._all_coins.append(Coin())
        self._all_coins.append(Coin())

        for player in self._all_players.values():
            if player._alive:
                self.find_empty_pos(entity=player)

        for coin in self._all_coins:
            self.find_empty_pos(entity=coin)

        for foe in self._all_foes:
            self.find_empty_pos(entity=foe)

        self.find_empty_pos(entity=self._next_level) 


    def update_all(self, player_id=None, dx=0, dy=0):
        """
        Met ?? jour tous les monstres, les joueurs et les coins.
        Si player_id != None, alors le joueur correspondant est boug?? de dx et de dy.

        :param player_id: l'id du joueur (None si aucun ne bouge)
        :param dx: d??placement en x du joueur
        :param dy: d??placement en y du joueur
        :return: les requ??tes ?? envoyer au joueur
        """

        if player_id is not None:
            if self._all_players[player_id]._alive == False:
                # il est mort, il ne peut rien faire
                return []

        packets = []

        if player_id is not None:
            player = self._all_players[player_id]
            if player is not None:
                data_player, ret_player = player.move(dx, dy, self)
                packets.append( (data_player, ret_player) )

        for coin in self._all_coins:
            id_collected = coin.check_collected(self)
            if not id_collected == None:
                coin.kill_entity(self)
                self._all_players[id_collected].earn_money(coin._value)
                packets.append( ((self.build_data_earn(id_collected, coin._value, self._all_players[id_collected]._money, self._all_players[id_collected]._score)), True) )

        for foe in self._all_foes:
            if foe._alive:
                packets_foe = foe.move_foe(self)
                packets.extend( packets_foe )

        id_next_level = self._next_level.check_collected(self)
        if id_next_level is not None:
            print("here")
            self._current_level += 1
            self._all_players[player_id]._score += 100
            self._next_level.kill_entity(self)
            packets.append(
                ((self.build_data_next_level(id_next_level, self._all_players[player_id]._score)), True)
            )

        return packets

    def attack(self, player_id):
        packets = []

        player = self._all_players[player_id]

        if player._alive == False:
            return packets

        for foe in self._all_foes:
            if foe._alive and foe.is_nearby(player):
                # on attaque ce monstre !
                data_fight = foe.attacked(self, 1)
                self._all_players[player_id]._score += foe.strength
                packets.append(data_fight)
                packets.append( (self.build_data_attack(foe.name, player_id, not foe._alive, self._all_players[player_id]._score), True) )

        for other_player in self._all_players.values():
            if other_player == player:
                continue
            if other_player._alive and other_player.is_nearby(player):
                # on attaque ce joueur
                packets.extend(other_player.attacked(self, 10, "Joueur " + str(player_id)))

        return packets

    def find_empty_pos(self, entity):
        """
        Trouve une position libre (ie un "..") sur la carte, puis l'ajoute ?? la carte.

        :param _map: la carte.
        :param entity: l'entit?? (un joueur, un monstre, etc.). Doit h??riter de Entity
        """
        n_row = len(self._map)
        n_col = len(self._map[0])

        y_init = randrange(n_row)
        # y_init = n_row // 2
        found = False
        while found is False:
            y_init += 1
            y_init %= n_row

            i = randrange(n_col)

            for incr in range(n_col):
                index_col = (i + incr) % n_col
                c = self._map[y_init][index_col]

                if c == "..":
                    x_init = index_col
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

    def build_data_earn(self, player_id, earned_amount, total, score):
        return [{"descr": "earn",
                 "ident": f"{player_id}",
                 "val": f"{earned_amount}",
                 "money": f"{total}",
                 "score": f"{score}"},
                {"foo": "bar"}]

    def build_data_attack(self, foe_name, player_id, is_dead, score):
        return [{"descr": "fight",
                 "ident": f"{player_id}",
                 "target": f"{foe_name}",
                 "isdead": f"{is_dead}",
                 "score": f"{score}"},
                {"foo": "bar"}]

    def build_data_dead(self, attacker_name, player_id, score):
        return [{"descr": "dead",
                 "attacker": f"{attacker_name}",
                 "ident": f"{player_id}",
                 "score": f"{score}"},
                {"foo": "bar"}]

    def build_data_damaged(self, attacker_name, amount, life, player_id):
        return [{"descr": "damaged",
                 "attacker": f"{attacker_name}",
                 "amount": f"{amount}",
                 "life": f"{life}",
                 "ident": f"{player_id}"},
                {"foo": "bar"}]

    def build_data_respawn(self, new_x, new_y, player_id, content):
        return [
            {
                "descr": "respawn",
                "i": f"{new_y}",
                "j": f"{new_x}",
                "life": "100",
                "ident": f"{player_id}",
                "content": f"{content}"
            }, 
            {"foo": "bar"}
        ]

    def build_data_new_challenger(self, x, y, player_id, content):
        return [
            {
                "descr": "new_challenger",
                "i": f"{y}",
                "j": f"{x}",
                "ident": f"{player_id}",
                "content": f"{content}"
            },
            {"foo": "bar"}
        ]

    def build_data_next_level(self, player_id, score):
        return [
            {
                "descr": "next_level",
                "ident": f"{player_id}",
                "no_new_level": f"{self._current_level}",
                "score": f"{score}"
            },
            {"foo": "bar"}
        ]

    def build_data_next_level_terrain(self):
        data_dict = {}
        data_dict["descr"] = "next_level_data"
        data_dict["max_y"] = self._h
        data_dict["max_x"] = self._w
        for y in range(self._h):
            data_dict[str(y)] = [""]*self._w
            for x in range(self._w):
                data_dict[str(y)][x] = self._map[y][x]

        return [
            data_dict, 
            {"foo": "bar"}
        ]

    def build_data_update_stats(self):
        data = {
                "descr": "update_stats",
                "level": self._current_level,
                "nb_joueurs": len(self._all_players),
        }
        player: Player
        for id, player in self._all_players.items():
            data["life"+str(id)] = "Life : " + str(player._life_pt) if player._alive else "Dead"
            data["gold"+str(id)] = "Gold : " + str(player._money)
            data["score"+str(id)] = "Score : " + str(player._score)
        
        return [
            data,
            {"foo": "bar"}
        ]