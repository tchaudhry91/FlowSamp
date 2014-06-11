#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mininet.cli import CLI
from mininet.link import Link
from mininet.log import lg
from mininet.net import Mininet
from mininet.node import Node, RemoteController
from mininet.topo import Topo


class TestTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        root = self.addHost('root', inNamespace=False)
        monitor = self.addHost('m1')
        source = self.addHost('s1')
        sink = self.addHost('s2')
        switch = self.addSwitch('sw1')

        self.addLink(monitor, switch)
        self.addLink(source, switch)
        self.addLink(sink, switch)
        self.addLink(monitor, root)

def configureRootConnection(root, monitor):
    root.setIP(intf="root-eth0", ip="10.0.1.2/24")
    monitor.setIP(intf="m1-eth1", ip="10.0.1.1/24")
    monitor.setIP(intf='m1-eth0', ip="10.0.0.1/24")
    monitor.setHostRoute(ip="10.0.0.2/24", intf="m1-eth1")
    monitor.cmd("ip route add 10.0.0.0/24 dev m1-eth0")
