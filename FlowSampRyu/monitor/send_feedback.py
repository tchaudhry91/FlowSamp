#! /usr/bin/python

import utilisation
import socket
import struct
from time import sleep
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser


def send_feedback(sock, ip, port, interface):
    """Build and Send Feedback to the Controller"""
    # Build
    # Observed Values
    link_data = utilisation.link_stats(interface)
    # Hardware Specifications (Read from config)
    parser = SafeConfigParser()
    parser.read('FlowSampRyu/monitor/monitor_specifications.ini')
    config_link_tp = int(parser.get('monitor_specifications',
                                    'max_link_tp'))
    max_link_tp = config_link_tp * 1024 ** 2  # 100 Mbit/sec
    # compute relative throughput
    rel_throughput = int(link_data['throughput'] * 100 / max_link_tp)
    packets_per_sec = link_data['packets/sec']
    message = struct.pack("!II", rel_throughput, packets_per_sec)
    print("Relative througput = " + str(rel_throughput))
    print("Packets per second = " + str(packets_per_sec))
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
        sleep(1)


if __name__ == "__main__":
    main()
