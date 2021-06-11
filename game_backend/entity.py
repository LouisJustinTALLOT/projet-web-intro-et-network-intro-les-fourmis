import random

symbol_coin = "o"

class Entity(object):
    def __init__(self, symbol):
        """
        Créé l'entité

        :param symbol: son symbole
        """
        self._x = None
        self._y = None
        self._symbol = symbol
        self._alive = True
        self.last_was_x = False

    def kill_entity(self, game):
        self._alive = False
        to_replace = "x" if self.last_was_x else "."
        game.getMap()[self._y][self._x] = to_replace
        data = game.build_data_displacement(-1, -1, " ", self._x, self._y, to_replace), True
        self._x = -1
        self._y = -1
        return data

    def is_nearby(self, entity):
        return self._x == entity._x and abs(self._y - entity._y) <= 1\
               or self._y == entity._y and abs(self._x - entity._x) <= 1


class Player(Entity):
    def __init__(self, id, symbol="@"):
        """
        Créé le joueur

        :param symbol: son symbole
        """
        super().__init__(symbol)
        self._id = id
        self._money = 0
        self._life_pt = 100

    def move(self, dx, dy, game):
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

        map = game.getMap()

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" or map[new_y][new_x] == symbol_coin:
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "x"
            data = game.build_data_displacement(new_x, new_y, self._symbol, self._x, self._y, "x")
            self._x = new_x
            self._y = new_y
        else:
            # n'a pas pu bouger
            ret = False
            data = []
        return data, ret

    def earn_money(self, _value):
        self._money += _value

    def attacked(self, game, damage, attacker_name):
        self._life_pt -= damage
        if self._life_pt <= 0:
            return [(game.build_data_dead(attacker_name, self._id), True), (self.kill_entity(game), True)]
        else:
            return [(game.build_data_damaged(attacker_name, damage, self._id), True)]


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
        super().__init__(symbol)

    def move_foe(self, game):
        """
        Déplace le monstre.
        Change la carte sur le serveur python.

        :param map: la carte.
        :return: la requête à envoyer au joueur pour afficher le déplacement
        """
        if not self._alive:
            return [], False

        this_was_x = False
        map = game.getMap()


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
                # on essaie quand même le dernier déplacement au cas-où (sauf si c'est un cul de sac...)
                last_try = (-self.last_displacement[0], -self.last_displacement[1])
                i, j = self._x + last_try[0], self._y + last_try[1]
                if map[j][i] in ['.', 'x']:
                    self.last_displacement = last_try
                    self._x = i
                    self._y = j

                    this_was_x = (map[j][i] == 'x')
                else:
                    return [], False

        to_replace = 'x' if self.last_was_x else '.'

        map[self._y][self._x] = self._symbol
        map[self._y - self.last_displacement[1]][self._x - self.last_displacement[0]] = to_replace

        data_foe = game.build_data_displacement(self._x, self._y, self._symbol, self._x - self.last_displacement[0], self._y - self.last_displacement[1], to_replace)

        self.last_was_x = this_was_x

        packets = self.attack(game)
        packets.insert(0, (data_foe, True))

        # on retourne une liste
        return packets

    def __repr__(self):
        return self.name[0]

    def attacked(self, game, damage):
        """
        A lancer lorsque ce monstre est attaqué
        :param game:
        :param damage: le montant des dommages
        :return:
        """
        print("previous lp :", self.pt_life)
        self.pt_life -= damage
        print("now lp :", self.pt_life)
        if self.pt_life <= 0:
            return self.kill_entity(game)
        else:
            return [], False

    def attack(self, game):
        """
        A lancer pour que ce monstre attaque.

        :param game:
        """

        packets = []

        for player in game._all_players.values():
            if player.is_nearby(self):
                packets.extend( player.attacked(game, self.strength, self.name) )

        # retourne une liste
        return packets


class Coin(Entity):
    def __init__(self):
        super(Coin, self).__init__(symbol=symbol_coin)
        self._value = 50

    def check_collected(self, game):
        """
        Indique si ce coin est collecté (attention, ne tue pas ce coin).

        :param game: game
        :return: l'id du joueur qui la collecte (ou None si aucun)
        """
        if self._alive:
            for player in game._all_players.values():
                if player._alive == True and self._x == player._x and self._y == player._y:
                    return player._id

        return None


