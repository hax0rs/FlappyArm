# FlappyArm

## About

Flappy Arm is a team based game in which a team of players
controls joints on a robotic arm to cooperatively pick up and move
objects. The aim of Flappy Arm is to inspire and educate younger students
about the multi-disciplinary effort required to create similar real world
robots and systems. Furthermore the arm acts as a proof of concept reflecting
on real world possibilities and applications including:

* Remote controlled surgical arms
* Remote controlled rescue robots / systems
* Education through demonstrations
* As an art installation

## Web Control Interface

The web interface is a simple user interface which allows
movement of a single motor on the robotic arm. The arm 
can be controlled using the slider on the webpage. Only 1
slider is provided on the webpage, as only 1 joint is to 
be controlled by 1 user.

The key features of the control interface are:

* Allows users to control a joint through a mobile optimise web interface
* Displays the currently selected control joint
* Ensures only one user can access a control point at any given time


## Robotic Arm

The Robotic Arm is based off the Robotic Arm with 7 Servos by jjshortcut.
The arm supports 6 Degrees of Freedome (DOF) through 7 motors allowing a
maximum of 7 concurrent players.    


## Installation

The program was developed in Python 3 and is not backwards compatible.
To run the control interface simply run `python3 main.py`
under main-controller.

### Dependencies / Requirements

* Python 3
* Flask
* flask-SocketIO
* pip3 install Flask-BasicAuth



## Contribute

If you would like to contribute to the project, you can find it on GitHub
at: (https://github.com/hax0rs/FlappyArm)[https://github.com/hax0rs/FlappyArm]


## Licensing and Copyright

Flappy are is licensed under the MIT license. For more information,
refer to LICENSE.