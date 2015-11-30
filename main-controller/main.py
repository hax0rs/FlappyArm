from flask import Flask, session, redirect, escape, request, render_template
from flask_socketio import SocketIO
# import subprocess
import os
import argparse
import sys
from arm_interface import ArmInterface



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
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', help='The host computer IP address.')
    arguments = parser.parse_args()
    HOST_IP = "localhost"
    if arguments.ip:
        HOST_IP = str(arguments.ip)
    # Run
    app.run(HOST_IP, threaded=True)
    socketio.run(app)
