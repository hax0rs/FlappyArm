import threading
import socket as sk
import os

ARM_CONFIG = "arm_config"
HOST = ""
PORT = "50007"


class ArmInterface(object):
    def __init__(self):
        self.server = ServerThread(self)
        self.kin = KinematicsThread(self)

        self.position = [0 for x in range(len(self.kin.load_arm_config()))]

    def begin_connection():
        self.server.start()

    def set_servo(num, percentage):
        self.server.lock.acquire()
        self.server.queue.append((num, percentage))
        self.server.lock.release()

    def reset_arm():
        pass


class ServerThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lock = threading.Lock()

        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.sock.bind((HOST, PORT))

        self.queue = []  # public queue, need lock to access this
        self._queue = []  # private queue, only accessed inside thread

    def run(self):
        self.sock.listen(1)
        print("Attempting connection to pi on separate thread...")
        self.conn, addr = self.sock.accept()
        print("Connected by", addr)
        data = self.conn.recv(1024)
        print(data.decode('utf-8'))

        while True:
            self.lock.acquire()
            if self.queue != []:
                self._queue.extend(self.queue)
            self.queue = []
            self.lock.release()

            for message in self._queue:
                print(message)  # send the message

        self.sock.close()
        print("pi thread exit")


class KinematicsThread(threading.Thread):
    """ Used to check the arm is not performing illegal moves
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lock = threading.Lock()
        self.servo_poi = self.load_arm_config()

    def run(self):
        print("kin thread ran")

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
                split_line = [int(x) for x in line.split(" ") if x != ""]
                data.append(split_line[1:])
        settings_file.close()
        return data
