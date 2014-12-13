FlowSamp
========
Source------OFSwitch-----Sink
             |    |
  Controller_|    |___Monitor
       |_______________|
         Feedback Link

Flow Samp is a flow sampling application which works by sampling the set of flows to be monitored in a particular topology.
The sampling is carried out based on a feedback loop between the controller and monitor which indicates the current load on the monitor.


Setup and Usage:

Pre-Requisites/Dependencies - mininet
                              ryu (Simple installation using 'pip install ryu')
                              openvswitch
                              bwm-ng
                              tcpreplay

Usage:
The app is simply launched using the 'flow_samp_testbed.py' script which in turns calls the other required scripts.
*Note - super user privileges required as it runs mininet internally.

The script then creates the above described topology inside mininet and start the ryu application and the monitor loop.

For debugging purposes, currently the controller app and the monitor loop are started manually (Commented out in the main script)

*Additional steps to debug/observe controller output
At the mininet command line, launch the following commands:

    xterm c0:
        (inside c0 xterm):
        'ryu-manager FlowSampRyu.controller.flow_samp'
   
    xterm m1:
        'FlowSampRyu/monitor/send_feedback.py 10.0.1.2 12000 m1-eth0'
                                Arguments = Cntr_IP  Port  Monitor_interface

    xterm s1
        'tcpreplay -i s1-eth0 /pathToPcap'
                (Use -x to multiply speed as required)
        './loadgen 10.0.0.4 num_flows delay time perflow_bandwidth'
                (Use to add synthetic flows, can be used in conjunction with tcpreplay)
