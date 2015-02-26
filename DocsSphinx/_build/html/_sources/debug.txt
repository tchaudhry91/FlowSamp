Debug/Developer Mode
********************

* This application can be a little hard to debug as the components do not present any output on the main application screen. To easily see all those debugging print statements please run the application as follows:

  * Run the flow_samp_testbed_debug.py instead of the normal one
  * This will not autostart any components in the systems (e.g monitor, controller etc.)
  * This must now be done manually using individual windows for each component so it is easy to observe their debug output
  * Take a look at the following lines commented out in the flow_samp_testbed_debug.py::

        root.cmd('ryu-manager FlowSampRyu.controller.flow_samp &')
        monitor.cmd('python2 FlowSampRyu/monitor/send_feedback.py' + 10.0.1.2 12000 m1-eth0 &')
        source.cmd('tcpreplay -i s1-eth0 -x ' + args.pcap_multiplier + ' ' + args.pcap + '  &')
        start_plotter('PlotLogs/values.log')

  * These lines must individually be executed on the corresponding different components:

        * Mininet should give you a prompt
        * Use this prompt to open terminals for the respective components::

            xterm m1
            xterm root
            xterm s1

        * You can then manually run the above mentioned commands in the terminal's of the respective components which will also provide debugging feedback
