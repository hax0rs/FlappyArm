import threading
import socket as sk
import os
from time import sleep

ARM_CONFIG = "arm_config"
HOST = ""
PORT = 12345


class ArmInterface(object):
    def __init__(self):
        self.server = ServerThread(self)
        self.kinematics = Kinematics(self)

        self.position = [0 for x in range(len(Kinematics.load_arm_config()))]

    def begin_connection(self):
        self.server.start()

    def set_servo(self, num, percentage):
        if percentage > 100:
            percentage = 100
        elif percentage < -100:
            percentage = -100

        if num < 0:
            num = 0
        elif num > 6:
            num = 6

        self._send_command(self.kinematics.get_servo(num, percentage))


    def reset_arm(self):
        servo_commands = []
        for i in range(len(Kinematics.load_arm_config())):
            servo_commands.extend(get_servo(i, 0))

        self._send_command(servo_commands)

    def _send_command(self, command):
        self.server.lock.acquire()
        self.server.queue.extend(command)
        self.server.lock.release()

        for num, percentage in command:
            self.position[num] = percentage

    def get_state(self):
        return self.position


class ServerThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lock = threading.Lock()

        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))

        self.queue = []  # public queue, need lock to access this
        self._queue = []  # private queue, only accessed inside thread

    def run(self):
        self.sock.listen(1)
        print("Attempting connection to pi on separate thread...")
        self.conn, addr = self.sock.accept()
        print("Connected on", addr)
        data = self.conn.recv(1024)
        print(data.decode('utf-8'))

        self.parent.reset_arm()

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
                # send the message
                self.conn.sendall((str(message[0]) + "_" + str(message[1]) + "|").encode('utf-8'))
            # empty the private queue
            self._queue = []

        self.sock.close()
        print("pi thread exit")


class Kinematics(object):
    """ Used to check the arm is not performing illegal moves and convert a
    percentage to angle.
    """

    def __init__(self, parent):
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

    def get_servo(self, num, percentage):
        i = 2
        if percentage <= 0:
            i = 1
        command = []
        for pin, mult in zip(self.pins[num], self.multipliers[num]):
            command.append((pin, mult[0] + round(percentage * mult[i])))
        return command

    @staticmethod
    def load_arm_config():
        """ Returns a list from the arm_config file
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
