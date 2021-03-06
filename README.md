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


![Main control interface for Flappyarm](https://raw.githubusercontent.com/hax0rs/FlappyArm/master/docs/img/control_interface.png "Main Control Interface")


The key features of the control interface are:

* Allows users to control a joint through a mobile optimise web interface
* Displays the currently selected control joint
* Ensures only one user can access a control point at any given time


## Robotic Arm

The Robotic Arm is based off the
["Robotic arm with 6 DOF" ancastrog.](http://www.thingiverse.com/thing:30163)
It is a 6 Degree of Freedom (DOF) arm with an extra axis for the pincer allowing
for 7 concurrent players. Currently the control system has not been
generalised as to allow any arm to be connected however it is a planned feature.
If you would like to connect an identical arm ensure that the scripts in the
'RPI' folder are stored and ran on the Raspberry Pi that is the main controller
of the arm.    


## Installation

The program was developed in Python 3 and is not backwards compatible.
To run the control interface simply run `python3 main.py`
under main-controller.

### Dependencies / Requirements

Please refer to `requirements.txt` in `backend/` and `rpi/` for a list of
packages which can be installed using `pip3 install -r requirements.txt`.



## Contribute

If you would like to contribute to the project, [you can find it on GitHub.](https://github.com/hax0rs/FlappyArm)


## Licensing and Copyright

FlappyArm is licensed under the MIT license. For more information,
refer to LICENSE.
