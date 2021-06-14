from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game

import pickle

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

player_id = -1

@socketio.on("login")
def send_player_id(json, methods=["GET", "POST"]):
    data = [
        {
            "descr": "send_player_id",
            "id": player_id
        },
        {"foo": "bar"}
    ]
    print("sending id to new player... ", player_id)
    socketio.emit("response", data)

    player = game._all_players[player_id]
    # à tous les autres joueurs, on doit envoyer le nouveau joueur
    socketio.emit("response", game.build_data_new_challenger(player._x, player._y, player_id, player._symbol))

@app.route("/")
def index():
    global player_id
    player_id = game.add_new_player()
    print("new player : ", player_id)

    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), players=game._all_players, n_players=game._nb_players )


@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    # print("received move ws message")
    dx = json['dx']
    dy = json["dy"]
    player_id = json["ident"]

    packets = game.update_all(player_id, dx, dy)

    for (data, ret) in packets:
        if ret:
            print(data)
            socketio.emit("response", data)

@socketio.on("attack")
def on_attack(json, methods=["GET", "POST"]):
    player_id = json["ident"]

    if game._all_players[player_id]._alive == False:
        return

    packets0 = game.attack(player_id)
    packets1 = game.update_all(None)

    for (data, ret) in packets0:
        if ret:
            socketio.emit("response", data)

    for (data, ret) in packets1:
        if ret:
            socketio.emit("response", data)

@socketio.on("respawn")
def on_respan(json, methods=["GET", "POST"]):
    player_id = json["ident"]
    player = game._all_players[player_id]

    if player._alive == False:
        # on ranime le joueur 
        player._alive = True
        player._life_pt = 100
        game.find_empty_pos(entity=player)
        
        data = game.build_data_respawn(player._x, player._y, player_id, player._symbol)
        socketio.emit("response", data)

@socketio.on("next_level_data_please")
def load_next_level_data(json, methods=["GET", "POST"]):
    if not game._current_level in game._dict_level_genere.keys():
        game.new_map()
        game._dict_level_genere[game._current_level] = True
    data = game.build_data_next_level_terrain()

    socketio.emit("response", data)

@socketio.on("sauvegarder")
def save_game_state(json, methods=["GET", "POST"]):
    if game._nb_players == 0:
        print("Saving game...")
        sauvegarde_jeu = pickle.dumps(game)
        with open("backup/my_backup", "wb") as file:
            file.write(sauvegarde_jeu)

@socketio.on("charger")
def load_game_state(json, methods=["GET", "POST"]):
    global game
    if game._nb_players == 0:
        print("Loading game...")
        with open("backup/my_backup", "rb") as file:
            sauvegarde_jeu = file.read()
        game = pickle.loads(sauvegarde_jeu)

    data = game.build_data_next_level_terrain()
    socketio.emit("response", data)
    data = game.build_data_update_stats()
    socketio.emit("response", data)



if __name__=="__main__":
    print("Starting app...")
    socketio.run(app, host="0.0.0.0", port=5001)


