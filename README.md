FlowSamp
Tanmay Chaudhry

SETUP:
VM Setup Instructions:
- Download VM From http://sourceforge.net/projects/ryu/files/vmimages/OpenFlowTutorial/
- (OpenFlow_Tutorial_Ryu3.6.ova)

- Startup VM (In Virtual Box, Import Appliance -> OVA) (Might consider adding Host-Only Adapter)

- sudo sed -i "s/\mirrors\.kernel\.org/old\-releases\.ubuntu\.com/g" /etc/apt/sources.list
- sudo sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
- Install (BWM-NG) (Write Script to install)
- Install TCP Replay

Demonstrator Application
