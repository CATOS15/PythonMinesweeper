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

class HTTPResponse:
    def __init__(self,msg,success):
        self.msg = msg
        self.success = success

    def toJSON (self):
        return json.dumps(self.__dict__)




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
    if(not data["name"] or not data["room"]["roomname"]):
        return  HTTPResponse('Udfyld venligst navn og rum',False).toJSON()

    removefromroom(request.sid)
    if(data["room"]["roomname"] in rooms):
        rooms[data["room"]["roomname"]][request.sid] = data["name"]
        join_room(data["room"]["roomname"])
        return HTTPResponse("Tilsluttet " + data["room"]["roomname"] + " med disse brugere " + str(rooms[data["room"]["roomname"]]),True).toJSON()
    else:
        return HTTPResponse("Rum findes ikke!",False).toJSON()

@socketio.on("createroom")
def createroom(jsondata):
    data = json.loads(jsondata)
    if(not data["name"] or not data["room"]["roomname"]):
        return  HTTPResponse('Udfyld venligst navn og rum',False).toJSON()

    removefromroom(request.sid)
    
    if(data["room"]["roomname"] in rooms):
        return HTTPResponse('Rummet findes ikke',False).toJSON()
    else:
        rooms[data["room"]["roomname"]] = {}
        rooms[data["room"]["roomname"]][request.sid] = data["name"]
        join_room(data["room"]["roomname"])
        return HTTPResponse('Rummet blev oprettet',True).toJSON()

@socketio.on("leaveroom")
def leaveroom():
    removefromroom(request.sid)

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
