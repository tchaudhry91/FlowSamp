#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.net import Mininet
from topology import TestTopo


def launch():
    """Start The Main Testbed"""
    # Build Topology
    topo = TestTopo()
    net = Mininet(topo=topo, controller=RemoteController)

    # Start Network
    net.start()

    # Start FlowSampApp
    controller = net.get('c0')
    switch = net.get('sw1')

    switch.cmd('ovs-vsctl set Bridge sw1 protocols=OpenFlow13')

    #controller.cmd('ryu-manager FlowSampRyu.flow_samp &')

    CLI(net)

    # Stop Network
    net.stop()


if __name__ == "__main__":
    launch()
