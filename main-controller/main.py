#!/usr/bin/python3
from flask import Flask, session, redirect, escape, request, render_template
from flask_socketio import SocketIO
import os
import argparse
import sys
from arm_interface import ArmInterface
from flask.ext.basicauth import BasicAuth
import uuid


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

# Routing
@app.route("/")
def home():
    return(render_template('home.html'))


@app.route("/about")
def about():
    return(render_template('about.html'))


@app.route("/play")
@app.route("/play/")
def play_menu():
    return ("Play menu.")


@app.route("/play/<int:controllerID>")
def root(controllerID=None):
    if 'user' in session:
        print (session['user'])
        print (global_list)
        
        if controllerID in global_list:
            if (session['user'] == global_list[controllerID]):
                return ("you can control")
            else:
                return ("someone is already controlling")
        else:
            a = uuid.uuid4()
            global_list[controllerID] = a
            session['user'] = a
            # return ("global_list)
            print (global_list)
            return("you're going to control.")   
    else:
        a = uuid.uuid4()
        global_list[controllerID] = a
        session['user'] = a
        # return ("global_list)
        print (global_list)
        return("you're going to control.")




    controller_name = {
        1: "Base",
        2: "Shoulder",
        3: "Elbow",
        4: "Wrist Rotation",
        5: "Wrist",
        6: "Pincer Rotation",
        7: "Pincer"
    }
    if (controllerID in controller_name):
        controller_name = str(controller_name[controllerID])
    else:
        controller_name = None
    return (render_template('control.html',
                            ip=HOST_IP,
                            controllerID=controllerID,
                            controller_name=controller_name))


@app.route("/in/")
def log_me_in():
    session['user'] = "dragan"
    return("should be logged now")



@app.route("/sessions/")
def get_sessions():
    return (session['user'])


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
