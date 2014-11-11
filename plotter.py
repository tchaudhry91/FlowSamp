#! /usr/bin/python
import sys
import matplotlib.pyplot as plt
from time import sleep
from FlowSampRyu.controller.limit_parser import limit_parser

PARAM_LIST = ['Bandwidth', 'Packet Count']
PARAM_COUNT = 3
SOFT_LIMIT = 0.9


def start_plotter(plot_log_file):
    """Starts an interactive plotter which plots figures for each parameter
        and the current accept limit
    """
    f_reader = open(plot_log_file, 'r')
    accept_limits = []
    param0_values = []
    param1_values = []

    limit_boundaries = limit_parser('FlowSampRyu/controller/sample.config')

    # Prepare Canvas
    plt.ion()
    fig = plt.figure()
    rect = fig.patch
    rect.set_facecolor('#31312e')
    count = 0
    while True:
        plt.clf()
        count = 0
        data = f_reader.read()
        f_reader.seek(0)
        for line in data.split('\n'):
            fields = line.split(';')
            if len(fields) < PARAM_COUNT:
                continue
            accept_limits.append(fields[0])
            param0_values.append(fields[1])
            param1_values.append(fields[2])
            count = count + 1

        if count > 15:
            count = 15
        # Plot Now

        # Accept Limit Plot
        ax1 = fig.add_subplot(2, 1, 2, axisbg='grey')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Accept Limit')
        ax1.plot(range(count), accept_limits[-count:], 'b-')
        ax1.set_xlim([0, 15])
        ax1.set_ylim([0, 105])
        ax1.tick_params(axis='x', colors='c')
        ax1.tick_params(axis='y', colors='c')
        ax1.set_title('Accept Limit Variations', color='c')

        # Bandwidth Plot
        ax2 = fig.add_subplot(2, 2, 1, axisbg='grey')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Utilisation')
        ax2.plot(range(count), param0_values[-count:], 'b-')
        ax2.set_xlim([0, 15])
        ax2.set_ylim([0, 105])
	ax2.plot([0, 15], [limit_boundaries[0], limit_boundaries[0]], 'r-')
	ax2.plot([0, 15], [(SOFT_LIMIT*limit_boundaries[0]), (SOFT_LIMIT*limit_boundaries[0])], 'y-')
        ax2.tick_params(axis='x', colors='c')
        ax2.tick_params(axis='y', colors='c')
        ax2.set_title('Bandwidth Utilisation', color='c')

        # Packet Limit Plot
        ax3 = fig.add_subplot(2, 2, 2, axisbg='grey')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Packets/Sec')
        ax3.plot(range(count), param0_values[-count:], 'b-')
        ax3.set_xlim([0, 15])
        ax3.tick_params(axis='x', colors='c')
        ax3.tick_params(axis='y', colors='c')
        ax3.set_title('Packets Limit', color='c')

        print 'Plotting'
        plt.draw()
        sleep(2)

if __name__ == "__main__":
    start_plotter(sys.argv[1])
