import argparse
import net_com
# import pigpio as pg


def main():
    usr_args = get_usr_args()
    net_client = net_com.Client(usr_args)


def get_usr_args():
    parser = argparse.ArgumentParser(description='Begin the arm controller')
    parser.add_argument('-ip', help='the ip of the host computer')
    parser.add_argument('-port', help='the ip of the host computer')
    return parser.parse_args()

if __name__ == '__main__':
    main()
