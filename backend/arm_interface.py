import threading
import socket as sk
import os
from time import sleep

ARM_CONFIG = "arm_config"  # name of configuration file for the arm
HOST = ""  # host IP, usually not needed because running on this machine
PORT = 12345  # port for communications with RPi


class ArmInterface(object):
    """High level class used to send commands to the arm."""
    def __init__(self):
        """Initialises server and arm kinematics classes."""
        self.server = _ServerThread(self)
        self.kinematics = _Kinematics(self)

        # self.position = [0 for x in range(len(_Kinematics.load_arm_config()))]

    def begin_connection(self):
        """Begins a connection to the RPi on a separate thread."""
        self.server.connect()
        self.reset_arm()  # reset arm on connection to lock all joints
        self.server.start()

    def set_servo(self, num, percentage):
        """Sets the value of a servo.

        Arguments:
        num -- the number of the servo (int)
        percentage -- the percentage of its full rotation for the servo
                      [-100, 100] (int)
        """
        percentage = int(percentage)
        num = int(num)
        self._send_command(self.kinematics.get_command(num, percentage))

    def reset_arm(self):
        """Resets arm to all zero points."""
        servo_commands = []
        for i in range(len(_Kinematics.load_arm_config())):
            servo_commands.extend(self.kinematics.get_command(i, 0))

        self._send_command(servo_commands)

    def _send_command(self, command):
        """Adds a command to the sending queue

        Arguments:
        command -- consists of "[pin]_[pulse]" to send to the arm (str)
        """
        self.server.lock.acquire()
        self.server.queue.extend(command)
        self.server.lock.release()

        # for num, percentage in command:
        #     self.position[num] = percentage

    def get_state(self):
        """Gets the current position of the arm. Not yet implemented"""
        pass
        # return self.position


class _ServerThread(threading.Thread):
    """Thread which sends commands to the RPi"""
    def __init__(self, parent):
        """Creates lock, socket and queue instances."""
        super().__init__()
        self.parent = parent
        self.lock = threading.Lock()

        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))

        self.queue = []  # public queue, need lock to access this
        self._queue = []  # private queue, only accessed inside thread

    def connect(self):
        """Connects to the RPi and receives a confirmation message."""
        self.sock.listen(1)
        print("Attempting to connect to RPi...")
        self.conn, addr = self.sock.accept()
        print("Connected on", addr)
        data = self.conn.recv(1024)
        print(data.decode('utf-8'))

    def run(self):
        """Enters a loop to send messages when they get added to the queue."""
        while True:
            self.lock.acquire()
            if self.queue != []:
                self._queue.extend(self.queue)
                self.queue = []
                self.lock.release()
            else:
                self.lock.release()
                sleep(0.005)
                continue

            for message in self._queue:
                print (message)
                # send the message
                write_string = ""
                for i, item in enumerate(message):
                    print (write_string)
                    write_string += str(item)
                    if not i == len(message) - 1:
                        write_string += "_"
                write_string += "|"
                self.conn.sendall(write_string.encode('utf-8'))
            # empty the private queue
            self._queue = []


class _Kinematics(object):
    """ Handles command validity checking and percent to pulse conversion."""
    def __init__(self, parent):
        """Loads arm configuration and calculates conversion multipliers for
        percentage to pulsewidth conversion.
        """
        self.servo_poi = self.load_arm_config()
        self.multipliers = []
        for poi in self.servo_poi:
            servo_set = []
            for poi_low, poi_mid, poi_high in zip(poi[1], poi[2], poi[3]):
                low = (poi_mid-poi_low)/100
                high = (poi_high-poi_mid)/100
                servo_set.append((poi_mid, low, high))
            self.multipliers.append(servo_set)
        self.pins = [x[0] for x in self.servo_poi]

    def get_command(self, num, percentage):
        """Calculates and checks the commands for the passed servo number and
        location percentage.

        Arguments:
        num -- the id number of the servo (int)
        percentage -- the percentage of rotation [-100, 100] (int)

        Returns:
        command -- a command in the form [pin, pulse] [(int), (int)]
        """
        if percentage > 100:
            percentage = 100
        elif percentage < -100:
            percentage = -100

        if num < 0:
            num = 0
        elif num > 6:
            num = 6

        i = 2
        if percentage <= 0:
            i = 1
        command = []
        for pin, mult in zip(self.pins[num], self.multipliers[num]):
            command.append((pin, mult[0] + round(percentage * mult[i])))
        return command

    @staticmethod
    def load_arm_config():
        """ Returns a list describing the arm configuration.
        """
        cwd = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(cwd, ARM_CONFIG)
        settings_file = open(full_path, "rU")
        data = []
        for line in settings_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            else:
                split_line = [eval(x) for x in line.split(" ") if x != ""]
                data.append(split_line[1:])
        settings_file.close()
        return data
