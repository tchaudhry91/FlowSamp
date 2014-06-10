import utilisation
import socket
from pickle import dumps
from time import sleep
from argparse import ArgumentParser
from common import feedback_message


def send_feedback(ip, port, interface):
    """Build and Send Feedback to the Controller"""
    # Build
    bandwidth = utilisation.link_utilisation(interface)
    message = feedback_message.FeedbackMessage(bandwidth=bandwidth)

    # Send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(message.dumps())
    s.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="Send Feedback to Controller")
    parser.add_argument("controllerIP", help="The Controllers IP")
    parser.add_argument("connectionPort",
                        help="Port on which controller is listening")
    parser.add_argument("monitorInterface")
    args = parser.parse_args()
    while(True):
        send_feedback(args.controllerIP,
                     int(args.connectionPort),
                     args.monitorInterface)
        sleep(10)
