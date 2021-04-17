from GameBoard import GameBoard
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
        "users": {
            "sid1": "kaj",
            "sid2": "ole"
        }
        "gameboard": {
            "hidden" = [
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.THREE][FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.ONE]  [FieldValue.ONE]
            ],
            "shown" = [
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.THREE][FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.ONE]  [FieldValue.HIDDEN]
            ],
            "newGame": False
            "width", 3,
            "height": 4,
            "mines": 3,
            "fieldsLeft", 1,
            "state": 0
        }
	},
	"room2": {
        "users": {
            "sid1": "brian",
            "sid2": "christian",
            "sid3": "tobias"
        }
        "gameboard": {
            "hidden" = [
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.THREE][FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.MINE]
                [FieldValue.BLANK][FieldValue.ONE]  [FieldValue.ONE]
            ],
            "shown" = [
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.THREE][FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.TWO]  [FieldValue.HIDDEN]
                [FieldValue.BLANK][FieldValue.ONE]  [FieldValue.HIDDEN]
            ],
            "newGame": False
            "width", 3,
            "height": 4,
            "mines": 3,
            "fieldsLeft", 1,
            "state": 0
        }
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

@socketio.on("sendmessage")
def sendmessage(jsondata):
    data_chatmessage = json.loads(jsondata)
    users = getUsersInRoom(data_chatmessage["roomname"])
    if(not request.sid in users):
        print("Brugeren (" + str(request.sid) + ") er ikke i rummet " + data_chatmessage["roomname"])
        return
        
    socketio.emit("emitMessage", json.dumps(data_chatmessage), room=data_chatmessage["roomname"])
    print(
        "Beskeden ( "
        + data_chatmessage["message"]
        + ' ) blev sendt til rum med id ' + data_chatmessage["roomname"]
    )
    
@socketio.on("leftClick")
def leftClick(jsondata):
    data_coordinate = json.loads(jsondata)
    users = getUsersInRoom(data_coordinate["roomname"])
    if(not request.sid in users):
        print("Brugeren (" + str(request.sid) + ") er ikke i rummet " + data_coordinate["roomname"])
        return

    gameboard = rooms[data_coordinate["roomname"]]["gameboard"]
    fields = gameboard.leftClick([], data_coordinate["x"], data_coordinate["y"])

    socketio.emit("emitClick", json.dumps(fields), room=data_coordinate["roomname"])
    socketio.emit("emitGamestate", gameboard.state.value, room=data_coordinate["roomname"])

@socketio.on("rightClick")
def rightClick(jsondata):
    data_coordinate = json.loads(jsondata)
    users = getUsersInRoom(data_coordinate["roomname"])
    if(not request.sid in users):
        print("Brugeren (" + str(request.sid) + ") er ikke i rummet " + data_coordinate["roomname"])
        return

    gameboard = rooms[data_coordinate["roomname"]]["gameboard"]
    fields = gameboard.rightClick(data_coordinate["x"], data_coordinate["y"])

    socketio.emit("emitClick", json.dumps(fields), room=data_coordinate["roomname"])

@socketio.on("refreshUsersConnected")
def refreshUsersConnected(jsondata):
    data_user = json.loads(jsondata)
    users = getUsersInRoom(data_user["room"]["roomname"])
    if(not request.sid in users):
        print("Brugeren (" + str(request.sid) + ") er ikke i rummet " + data_user["room"]["roomname"])
        return

    return emitUsersConnected(data_user["room"]["roomname"])

@socketio.on("getshownfields")
def getshownfields(jsondata):
    data_user = json.loads(jsondata)
    users = getUsersInRoom(data_user["room"]["roomname"])
    if(not request.sid in users):
        print("Brugeren (" + str(request.sid) + ") er ikke i rummet " + data_user["room"]["roomname"])
        return

    gameboard = rooms[data_user["room"]["roomname"]]["gameboard"]
    fields = gameboard.getShownFields()

    socketio.emit("emitGamestate", gameboard.state.value, room=data_user["room"]["roomname"])
    return HTTPResponse(json.dumps(fields),True).toJSON()

@socketio.on("joinroom")
def joinroom(jsondata):
    data_user = json.loads(jsondata)
    if(not data_user["name"] or not data_user["room"]["roomname"]):
        return HTTPResponse('Udfyld venligst navn og rum',False).toJSON()

    removefromroom(request.sid)
    if(not data_user["room"]["roomname"] in rooms):
        return HTTPResponse("Rum findes ikke!",False).toJSON()

    rooms[data_user["room"]["roomname"]]["users"][request.sid] = data_user["name"]
    join_room(data_user["room"]["roomname"])

    gameboard = rooms[data_user["room"]["roomname"]]["gameboard"]
    response = {'width':gameboard.width,'height':gameboard.height}

    return HTTPResponse(json.dumps(response),True).toJSON()


@socketio.on("createroom")
def createroom(jsondata):
    data_user = json.loads(jsondata)
    if(not data_user["name"] or not data_user["room"]["roomname"]):
        return HTTPResponse('Udfyld venligst navn og rum',False).toJSON()

    removefromroom(request.sid)
    
    if(data_user["room"]["roomname"] in rooms):
        return HTTPResponse('Rummet findes ikke',False).toJSON()

    rooms[data_user["room"]["roomname"]] = {
        "users": {},
        "gameboard": None,
    }
    rooms[data_user["room"]["roomname"]]["users"][request.sid] = data_user["name"]
    join_room(data_user["room"]["roomname"])

    gameboard = getNewGameboard(data_user["room"]["difficulty"])
    rooms[data_user["room"]["roomname"]]["gameboard"] = gameboard

    response = {'width':gameboard.width,'height':gameboard.height}
    return HTTPResponse(json.dumps(response),True).toJSON()

@socketio.on("leaveroom")
def leaveroom():
    removefromroom(request.sid)

@socketio.on("disconnect")
def ondisconnect():
    removefromroom(request.sid)

def removefromroom(sid):
    for roomname in rooms:
        if(sid in rooms[roomname]["users"]):
            print("Bruger " + rooms[roomname]["users"][sid] + " afbrød forbindelsen til rummet " + roomname)
            del rooms[roomname]["users"][sid]
            emitUsersConnected(roomname)
            if len(rooms[roomname]["users"]) == 0:
                print("Da et rum er tomt slettes dette " + roomname)
                close_room(roomname)
                del rooms[roomname]
            return True
    return False

def emitUsersConnected(roomname):
    usernames = []
    for sid in getUsersInRoom(roomname):
        username = rooms[roomname]["users"][sid]
        usernames.append(username)
    socketio.emit("emitUsersConnected", json.dumps(usernames), room=roomname)
    return usernames

def getUsersInRoom(roomname):
    if(not roomname in rooms):
        print("Intet rum med id: " + roomname)
        return {}
    return rooms[roomname]["users"]


def getNewGameboard(difficulty):
    mines = 0
    width = 0
    height = 0

    if difficulty == 0:
        mines = 10
        width = 10
        height = 8
    elif difficulty == 1:
        mines = 40
        width = 14
        height = 18
    elif difficulty == 2:
        mines = 99
        width = 24
        height = 20
    return GameBoard(width,height,mines)




if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5005, debug=True)