import utilisation
import socket
import struct
from time import sleep
from argparse import ArgumentParser


def send_feedback(socket, ip, port, interface):
    """Build and Send Feedback to the Controller"""
    # Build
    bandwidth = utilisation.link_utilisation(interface)
    message = struct.pack("!I", bandwidth)
    sock.sendto(message, (ip, port))


if __name__ == "__main__":
    parser = ArgumentParser(description="Send Feedback to Controller")
    parser.add_argument("controllerIP", help="The Controller's IP")
    parser.add_argument("connectionPort",
                        help="Port on which controller is listening")
    parser.add_argument("monitorInterface")
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    while(True):
        send_feedback(sock, args.controllerIP,
                     int(args.connectionPort),
                     args.monitorInterface)
        sleep(10)
