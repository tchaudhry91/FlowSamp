#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.net import Mininet
from topology import TestTopo, configureRootConnection
from plotter import start_plotter
from argparse import ArgumentParser

def launch():
    """Start The Main Testbed"""
    parser = ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()	
	
    # Build Topology
    topo = TestTopo()
    net = Mininet(topo=topo, controller=RemoteController)

    # Start Network
    net.start()

    # Start FlowSampApp
    root = net.get('root')
    monitor = net.get('m1')
    switch = net.get('sw1')
    source = net.get('s1')

    switch.cmd('ovs-vsctl set Bridge sw1 protocols=OpenFlow13')
    configureRootConnection(root, monitor)

    root.cmd('ryu-manager FlowSampRyu.controller.flow_samp &')
    monitor.cmd('python2 FlowSampRyu/monitor/send_feedback.py 10.0.1.2 12000 m1-eth0 &')
    source.cmd('tcpreplay -i s1-eth0 -x ' + args.pcap_multiplier + ' ' + args.pcap + '  &')

    start_plotter('PlotLogs/values.log')

    # Stop Network
    net.stop()

def add_arguments(parser):
    """Add and Parse command Line Options"""
    parser.add_argument("pcap", help=("The Pcap File you would like to Replay"))
    parser.add_argument("pcap_multiplier", help=("The rate at which the Pcap should be replayed"))

if __name__ == "__main__":
    launch()
