from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minesw!eper_miss3kat'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def hello():
    return "Test deployment backend"

@app.route('/sockettest/<msg>')
def sockettest(msg):
    socketio.emit('emitTest', 
    {
        'data': msg
    })
    return 'Beskeden ( ' + msg + ' ) blev sendt til alle der er connected til "emitTest" eventet'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005)