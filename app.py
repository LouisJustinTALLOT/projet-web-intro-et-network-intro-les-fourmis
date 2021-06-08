from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    data_player, ret_player, data_foe, ret_foe = game.move_all(dx, dy)

    if ret_player:
        socketio.emit("response", data_player)

    if ret_foe:
        socketio.emit("response", data_foe)


if __name__=="__main__":
    socketio.run(app, port=5001)


