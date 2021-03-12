from flask import Flask, request
from flask_socketio import SocketIO, close_room, join_room, leave_room
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "minesw!eper_miss3kat"
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=10, ping_interval=5)

"""
Dette er et eksempel på hvordan 'rooms' objektet ser ud
rooms: {
	"room1": {
		"sid1": "kaj",
		"sid2": "ole"
	},
	"room2": {
		"sid1": "hans",
		"sid2": "svend"
	},
	"room3": {
		"sid1": "brian",
		"sid2": "christian",
		"sid3": "tobias"
	}
}
"""
rooms = {}

@app.route("/")
def default():
    return ""


@app.route("/sendmessage/<to>/<msg>")
def sendmessage(to, msg):
    socketio.emit("emitTest", {"data": msg}, room=to)
    return (
        "Beskeden ( "
        + msg
        + ' ) blev sendt til rum/person med id ' + to
    )

@socketio.on("joinroom")
def joinroom(jsondata):
    data = json.loads(jsondata)
    removefromroom(request.sid)
    if(data["roomname"] in rooms):
        rooms[data["roomname"]][request.sid] = data["name"]
        join_room(data["roomname"])
        return "Tilsluttet " + data["roomname"] + " med disse brugere " + str(rooms[data["roomname"]])
    else:
        return "Rum findes ikke!"

@socketio.on("createroom")
def createroom(jsondata):
    data = json.loads(jsondata)
    removefromroom(request.sid)
    if(data["roomname"] in rooms):
        return "Rummet findes allerede"
    else:
        rooms[data["roomname"]] = {}
        rooms[data["roomname"]][request.sid] = data["name"]
        join_room(data["roomname"])
        return "Rummet blev oprettet"


@socketio.on("disconnect")
def ondisconnect():
    removefromroom(request.sid)

def removefromroom(sid):
    for roomname in rooms:
        room = rooms[roomname]
        if(request.sid in room):
            print("Bruger " + rooms[roomname][sid] + " afbrød forbindelsen med rummet " + roomname)
            del rooms[roomname][sid]
            if len(rooms[roomname]) == 0:
                print("Da et rum er tomt slettes dette " + roomname)
                close_room(roomname)
                del rooms[roomname]
            return True

    return False

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5005)
