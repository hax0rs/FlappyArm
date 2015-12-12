import argparse
import socket as sk
import threading
import pigpio as pg
from time import sleep

NETWORK_CONFIG = "network_config"  # file which stores the IP and port of host

PI = pg.pi()  # creates a raspberry Pi object to access GPIOs


class Client(object):
    """Client class handles settings and contains instances of the
    ServoWriter and NetworkThread
    """
    def __init__(self, usr_args):
        """Updates network settings based on user arguments. Creates instances
        of necessary classes for communication and servo writing.

        Arguments:
        usr_args -- the namespace of user arguments as returned by the python
            argument parser

        Returns:
        None
        """

        self.net_settings = self.update_net_settings(usr_args)
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

        self.network_thread = NetworkThread(self)
        self.servo_writer = ServoWriter(self.network_thread.lock)

    def begin(self):
        """Attempts to open a connection to the host computer. Begins the
        loops for communication and servo writing.

        Returns:
        None
        """

        while True:
            try:
                self.sock.connect(self.net_settings)
                break
            except Exception as err:
                print("Connection failed with error: " + str(err))
                sleep(1)
                print("Trying again...")

        self.sock.sendall("RPi client initialised".encode('utf-8'))

        self.network_thread.start()
        self.servo_writer.control_loop()

    def update_net_settings(self, usr_args):
        """ Updates network settings.

        Returns:
        ip -- the currently defined ip (str)
        port -- the currently defined port (int)
        """
        ip = None
        port = None

        try:
            fd = open(NETWORK_CONFIG)
            ip = fd.readline()
            port = int(fd.readline())
        except:
            pass

        try:
            fd.close()
        except:
            pass

        if usr_args.ip is not None:
            ip = usr_args.ip
        if usr_args.port is not None:
            port = int(usr_args.port)

        msg_strings = []
        if not ip:
            msg_strings.append("IP")
        if not port:
            msg_strings.append("PORT")

        if ip is None or port is None:
            error_string = "A valid "
            for item in range(len(msg_strings) - 1):
                error_string += item
            error_string += " and " + msg_strings[-1]
            error_string += ("has not been specified. Please enter them as" +
                             "inline arguments")
            raise Exception(error_string)

        fd = open(NETWORK_CONFIG, "w")
        fd.write(ip + "\n")
        fd.write(str(port))

        return (ip, port)


class NetworkThread(threading.Thread):
    """Thread which receives instructions from the host computer. Runs in
    parallel with the rest of the program.
    """
    def __init__(self, parent):
        """Initialises thread and creates a lock."""
        super().__init__()
        self.parent = parent
        self.lock = threading.Lock()

    def run(self):
        """Runs a network receiving loop, writing to the ServoWriter queue."""
        print("Network loop initiated on RPi")

        while True:
            message = self.parent.sock.recv(1024)
            self.lock.acquire()
            self.parent.servo_writer.queue.append(message)
            self.lock.release()


class ServoWriter(object):
    """Handles the GPIO pin commands needed to control the arm"""
    def __init__(self, lock):
        """Creates queue and writes lock to local namespace for easy accessing.

        Arguments:
        lock -- Lock required to access instruction queue (threading.Lock())
        """
        self.queue = []
        self._queue = []

        self.lock = lock

    def control_loop(self):
        """Continually acquires lock, checks for instructions and executes
        them. This is the main loop of the program.
        """
        while True:
            self.lock.acquire()
            if self.queue != []:
                self._queue.extend(self.queue)
                self.queue = []
                self.lock.release()
            else:
                self.lock.release()
                sleep(0.005)

            for cmd in self._queue:
                cmd = cmd.decode('utf-8')
                cmd = [x for x in cmd.split("|") if x != ""]
                for command in cmd:
                    pin, pulse = [int(x) for x in command.split("_")]
                    PI.set_servo_pulsewidth(pin, pulse)
                    print("Servo {0}: {1}".format(pin, pulse))
            self._queue = []


def main():
    parser = argparse.ArgumentParser(description='Begin the arm controller')
    parser.add_argument('-ip', help='the ip of the host computer')
    parser.add_argument('-port', help='the ip of the host computer')
    usr_args = parser.parse_args()
    client = Client(usr_args)
    client.begin()


if __name__ == '__main__':
    main()
