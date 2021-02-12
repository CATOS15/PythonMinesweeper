from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Test deployment backend"

if __name__ == '__main__':
    app.run()