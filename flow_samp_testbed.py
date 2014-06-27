#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.net import Mininet
from topology import TestTopo, configureRootConnection


def launch():
    """Start The Main Testbed"""
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

    # controller.cmd('ryu-manager FlowSampRyu.controller.flow_samp &')
    # monitor.cmd('/FlowSampRyu/monitor/send_feedback.py 10.0.1.2 12000 m1-eth1')
    # s1.cmd('tcpreplay -i s1-eth0 pcap/13-03-2013-anon.pcap')
    

    CLI(net)

    # Stop Network
    net.stop()


if __name__ == "__main__":
    launch()
