#!/bin/bash

set -o nounset

if [ $# -ne 5 ]
then
    echo "Usage: `basename $0` {destIP} {num of flows} {delay between flows} {time in s} {per flow bandwidth M}"
    /bin/bash
fi

DEST=$1
NUMFLOWS=$2
DELAY=$3
LEN=$4
BAND=$5
i=0
while [ $i -ne $NUMFLOWS ]; do
    sleep $DELAY
    ((i++))
    port=$((1337+$i))
    iperf -c $DEST --udp --port $port --len 64 -t $LEN  -b "$BAND"M 
done
#/bin/bash
#optionally on the other side
#iperf -s -u --port 1337
