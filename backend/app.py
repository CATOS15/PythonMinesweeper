from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, close_room
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "minesw!eper_miss3kat"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def hello():
    return "Test deployment backend"


@app.route("/sockettest/<roomname>/<msg>")
def sockettest(roomname, msg):
    socketio.emit("emitTest", {"data": msg}, room=roomname)
    return (
        "Beskeden ( "
        + msg
        + ' ) blev sendt til alle der er connected til "emitTest" eventet'
    )


@socketio.on("joinroom")
def joinroom(jsondata):
    data = json.loads(jsondata)
    join_room(data["roomname"])


@socketio.on("createroom")
def createroom(jsondata):
    data = json.loads(jsondata)
    join_room(data["roomname"])


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5005)
