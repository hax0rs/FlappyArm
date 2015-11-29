from flask import Flask, session, redirect, escape, request, render_template
from flask_socketio import SocketIO
# import subprocess
import os
from arm_interface import ArmInterface

# Global Variables and Declarations
HOST_IP = "131.181.68.177"


script_path = os.path.abspath('external_test_script.py') 

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app)

# Connect to Arm
arm = ArmInterface()
arm.begin_connection()

@app.route("/")
@app.route("/<int:controllerID>")
def root(controllerID=None):
    return (render_template('control.html', ip=HOST_IP, controllerID=controllerID))


@socketio.on('json')
def handle_json(json):
    """ Handles the values received from the slider.
    :json: Dictionary - {'id':servoID,'value':value(-100,100)}
    :return: None
    """
    # Controlling the arm
    arm.set_servo(json['id'], json['value'])

    print ("This is controller: " + str(json['id']))
    print ("The value for this motor is:  " + str(json['value']))


@app.route("/leaderboard/")
def leaderboard():
    return ("<ol><li>UQ hax0rs</li></ol>")


if __name__ == "__main__":
    # app.debug = True
    app.secret_key = 'such_secret_very_secure'
    app.run(host=HOST_IP, threaded=True)
    socketio.run(app)
