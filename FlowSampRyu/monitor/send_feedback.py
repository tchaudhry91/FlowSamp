#! /usr/bin/python

import utilisation
import socket
import struct
from time import sleep
from argparse import ArgumentParser


def send_feedback(sock, ip, port, interface):
    """Build and Send Feedback to the Controller"""
    # Build
    bandwidth = utilisation.link_utilisation(interface)
    packets_total = utilisation.packets_total(interface)
    message = struct.pack("!II", bandwidth, packets_total)
    print("Bandwidth = " + str(bandwidth))
    print("Packets Total = " + str(packets_total))
    sock.sendto(message, (ip, port))


def main():
    """The main function"""
    parser = ArgumentParser(description="Send Feedback to Controller")
    parser.add_argument("controllerIP", help="The Controller's IP")
    parser.add_argument("connectionPort",
                        help="Port on which controller is listening")
    parser.add_argument("monitorInterface")
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    while True:
        send_feedback(sock, args.controllerIP,
                     int(args.connectionPort),
                     args.monitorInterface)
        sleep(2)


if __name__ == "__main__":
    main()
