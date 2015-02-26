FlowSampling Demonstrator Tutorial
**********************************

SETUP: Note - All commands 'sudo' unless otherwise specified. VM Setup Instructions:

* Download VM From http://sourceforge.net/projects/ryu/files/vmimages/OpenFlowTutorial/

  * Choose Image : OpenFlow_Tutorial_Ryu3.6.ova
  * Setup the VM in Virtual Box:

    *  Import Appliance -> OVA
    * Add a Host-Only Network Adapter (Varies on Different Operating Systems). This will be used to SSH into this machine.
    * Boot up the VM, (user - ryu, password - ryu)
    * Clone the Repository, you may also consider copying over the Pcap which you wish to replay.
    * This application requires 'tcpreplay' and 'bwm-ng'. There is a requirement installation script which will take care of all the pre-requisites::

        sudo ./requirement_install_script.sh

  * Setup Should Now be Complete

* Demonstrator Application

  * The Demonstrator requires working 'X' Server. The default installation does not come with one, however ssh -X works fine and can be used. So 'ssh -X ryu@xyzhost' should suffice.
  * For the basic Demonstrator, just run the following::

        ./flow_samp_testbed.py pcap pcap_multiplier (use -h for more info)

  * The following options can be changed:

        * Pcap -> The file you want to replay -> Can be changed as a command line argument.
        * Pcap Multiplier -> The multiplier at which the pcap should be replayed.
        * Limits -> Edit the file in FlowSampRyu/controller/sample.config (Keep the same structure)
  * IMPORTANT -> Should you use Ctrl+C to kill the application, not all internal applications will be killed. So use the ./cleanup.sh script to clean up before re-running.
