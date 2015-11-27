from flask import Flask
from flask_socketio import SocketIO
import subprocess
import os

# External test script with absolute path
full_path = os.path.abspath('external_test_script.py')


app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def root():
    return ("<a>go to /play/</a>")

@app.route("/play/")
def play():
    os.system("say hello world")
    subprocess.call(full_path)
    return "Hello World!"


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print ("actual text: " + str(json['data']))

@app.route("/leaderboard/")
def leaderboard():
    return ("<ol><li>UQ hax0rs</li></ol>")

if __name__ == "__main__":
    app.debug = True
    app.run(host='192.168.0.99')
    socketio.run(app)



