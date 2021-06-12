from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), players=game._all_players, n_players=len(game._all_players) )

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
    packets0 = game.attack(player_id)
    packets1 = game.update_all(None)

    for (data, ret) in packets0:
        if ret:
            socketio.emit("response", data)

    for (data, ret) in packets1:
        if ret:
            socketio.emit("response", data)


if __name__=="__main__":
    socketio.run(app, port=5001)


