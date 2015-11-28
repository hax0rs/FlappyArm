import argparse
# import pigpio as pg


def main():
    update_network_settings()


def update_network_settings():
    parser = argparse.ArgumentParser(description='Begin the arm controller')
    parser.add_argument('ip', help='the ip of the host computer')
    parser.add_argument('port', help='the ip of the host computer')
    network = parser.parse_args()

    print(network.ip)
    print(network.port)

if __name__ == '__main__':
    main()
