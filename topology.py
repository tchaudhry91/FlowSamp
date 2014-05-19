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

        monitor = self.addHost('m1')
        source = self.addHost('s1')
        sink = self.addHost('s2')
        switch = self.addSwitch('sw1')

        self.addLink(monitor, switch)
        self.addLink(source, switch)
        self.addLink(sink, switch)
