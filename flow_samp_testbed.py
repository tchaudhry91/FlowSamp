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

    # Stop Network
    net.stop()
