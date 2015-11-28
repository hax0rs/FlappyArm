import argparse
import socket as sk
import threading
from time import sleep
# import pigpio as pg

NETWORK_CONFIG = "network_config"

def main():
    parser = argparse.ArgumentParser(description='Begin the arm controller')
    parser.add_argument('-ip', help='the ip of the host computer')
    parser.add_argument('-port', help='the ip of the host computer')
    usr_args = parser.parse_args()
    Client(usr_args)


class Client(object):
    def __init__(self, usr_args):
        net_settings = self.update_net_settings(usr_args)
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        while True:
            try:
                self.sock.connect(net_settings)
                break
            except Exception as err:
                print("Connection failed with error: " + str(err))
                sleep(1)
                print("Trying again...")

        self.sock.sendall("Hello, coming in from the Arm Pi".encode('utf-8'))
        self.begin_command_loop()

        self.network_thread = NetworkThread(self)
        self.servo_writer = ServoWriter(self.network_thread.lock)

    def update_net_settings(self, usr_args):
        try:
            fd = open(NETWORK_CONFIG)
            ip = fd.readline()
            port = int(fd.readline())
        except:
            ip, port = None, None
        try:
            fd.close()
        except:
            pass
        if usr_args.ip is not None:
            ip = usr_args.ip
        if usr_args.port is not None:
            port = int(usr_args.port)

        if ip is None or port is None:
            raise Exception("Please specify a valid IP and port when running the script")

        fd = open(NETWORK_CONFIG, "w")
        fd.write(ip + "\n")
        fd.write(str(port))

        return (ip, port)


class NetworkThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.lock = threading.Lock()

    def run(self):
        print("Network connection loop initiated on auxiliary thread")

        while True:
            message = self.parent.sock.recv(1024).decode('utf-8')
            if message != "reset":
                self.lock.acquire()
                

class ServoWriter(object):
    def __init__(self, lock):
        self.queue = []
        self._queue = []




if __name__ == '__main__':
    main()


