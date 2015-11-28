import socket as sk
import threading
from time import sleep

NETWORK_CONFIG = "network_config"

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

    def update_net_settings(self, usr_args):
        fd = open(NETWORK_CONFIG)
        try:
            ip = fd.readline()
            port = int(fd.readline())
        except:
            ip, port = None, None
        fd.close()
        if usr_args.ip is not None:
            ip = usr_args.ip
        if usr_args.port is not None:
            port = usr_args.port

        if ip is None or port is None:
            raise Exception("Please specify a valid IP and port when running the script")

        fd = open(NETWORK_CONFIG, "w")
        fd.write(ip + "\n")
        fd.write(str(port))

        return (ip, port)
