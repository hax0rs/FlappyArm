import pigpio as io
import socket
from time import sleep

VERSION = float(1.0)

pi = io.pi()

HOST = "169.254.101.80"
PORT = 50007


def load_config_file(filename):
    """ Returns a dictionary containing the configuration elements in the file:
    'filename' contained in the subfolder of the cwd: 'folder'.

    load_config_file(str, str) -> dict
    """
    settings_file = open(filename, "r")
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


class Client(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        connect_message = 'RPI Connected on: ' + str(self.s.getsockname()) + '\n' \
                          + 'Running ARM_SIM V{0}'.format(VERSION)
        self.s.sendall(connect_message.encode('utf-8'))

    def send(self, string):
        self.s.sendall(string.encode('utf-8'))

    def send_beat(self):
        self.s.sendall('1'.encode('utf-8'))

    def recieve(self):
        data = self.s.recv(1024)
        data = data.decode('utf-8')
        data_list = []
        for element in data.split():
            if element.isdigit():
                data_list.append(int(element))
            else:
                try:
                    data_list.append(float(element))
                except ValueError:
                    data_list.append(element)

        if data_list[0] == 's':
            return self.recieve_servo(data_list)

        return data_list

    def recieve_servo(self, data):
        try:
            _, pin, pulse = data
            pi.set_servo_pulsewidth(pin, pulse)
            print("write: {0}, {1}".format(pin, pulse))
        except:
            pass


def main():
    servo_data = load_config_file("servo_poi")

    for data in servo_data:
        try:
            pi.set_servo_pulsewidth(data[0], data[2])
        except:
            pass

    while True:
        try:
            client = Client()
            break
        except:
            sleep(0.1)

    while True:
        client.send_beat()
        client.recieve()

if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass
