import threading
import socket as sk
import os

ARM_CONFIG = "arm_config"


class ArmInterface(object):
    def __init__(self):
        self.serv_lock = threading.Lock()
        self.server = ServerThread(self)
        self.kin_lock = threading.Lock()
        self.kin = KinematicsThread(self)


class ServerThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lock = parent.serv_lock

    def run(self):
        print("kin thread ran")


class KinematicsThread(threading.Thread):
    """ Used to check the arm is not performing illegal moves
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.lock = parent.kin_lock

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
