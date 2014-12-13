#!/bin/sh

sudo killall ryu-manager
sudo killall tcpreplay
sudo mn -c
: >  PlotLogs/values.log
