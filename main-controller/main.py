from flask import Flask, session, redirect, url_for, escape, request
from flask_socketio import SocketIO
import subprocess
import os

# Global Variables and Declarations
HOST_IP = "192.168.0.99"
script_path = os.path.abspath('external_test_script.py')

app = Flask(__name__)
socketio = SocketIO(app)

test_list = []


@app.route("/")
@app.route("/<controller>")
def root(controller=None):
    if (controller is None):
        return ("Sorry, you cannot play.")
    else:
        os.system("say hello world")
        subprocess.call(script_path)
        return ("Hello Controller" + str(controller) + "!")


@socketio.on('my event')
def handle_my_custom_event(message):
    print (message)
    # os.system("say youre accessing this in browser")


@app.route("/leaderboard/")
def leaderboard():
    return ("<ol><li>UQ hax0rs</li></ol>")


if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'such_secret_very_secure'
    app.run(host=HOST_IP, threaded=True)
    socketio.run(app)
