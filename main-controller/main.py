#!/usr/bin/python3
from flask import Flask, session, redirect, escape, request, render_template
from flask_socketio import SocketIO
import os
import argparse
import sys
from arm_interface import ArmInterface
from flask.ext.basicauth import BasicAuth
# import uuid
import players

app = Flask(__name__, static_folder="static")
# Auth
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
basic_auth = BasicAuth(app)
socketio = SocketIO(app)

# Connect to Arm
# arm = ArmInterface()
# arm.begin_connection()

global_list = {}

current_players = players.Players()


# Routing
@app.route("/")
def home():
    return(render_template('home.html'))



@app.route("/play")
@app.route("/play/")
def play_menu():
    current_players.garbage_collector()
    return (str(current_players._players))


@app.route("/play/<int:controllerID>", methods=["GET"])
def root(controllerID=None):
    request_ip = str(request.remote_addr)
    if 'user' in session:
        if controllerID in current_players.get_players():
            if (session['user'] == current_players.get_players()[controllerID]._cookie):
                return ("you can control.")
            else:
                return ("someone is already controlling")
        else:
            current_players.add_player(controllerID,players.Player(request_ip))
            print(current_players.get_players()[controllerID]._cookie)
            session['user']= current_players.get_players()[controllerID]._cookie
            return ("you're going to control")            
    else:
        current_players.add_player(controllerID, players.Player(request_ip))
        print()
        session['user']= current_players.get_players()[controllerID]._cookie
        return ("you're going to control")            



    controller_name = {
        0: "Base",
        1: "Shoulder",
        2: "Elbow",
        3: "Wrist Rotation",
        4: "Wrist",
        5: "Pincer Rotation",
        6: "Pincer"
    }
    if (controllerID in controller_name):
        controller_name = str(controller_name[controllerID])
    else:
        controller_name = None
    return (render_template('control.html',
                            ip=HOST_IP,
                            controllerID=controllerID,
                            controller_name=controller_name))




@app.route("/leaderboard")
def leaderboard():
    return ("<ol><li>UQ hax0rs</li></ol>")


@app.route('/admin')
@app.route('/admin/')
@basic_auth.required
def admin():
    return ("Admin page.")


# Sockets
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


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', help='The host computer IP address.')
    arguments = parser.parse_args()
    HOST_IP = "localhost"
    if arguments.ip:
        HOST_IP = str(arguments.ip)
    app.secret_key = "change_this_to_something_better"
    app.run(HOST_IP, threaded=True, debug=True)
    socketio.run(app)
