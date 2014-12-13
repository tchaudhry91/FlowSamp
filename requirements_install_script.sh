sudo sed --in-place=.old -e 's/mirrors.kernel.org|archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

sudo apt-get update
sudo apt-get install bwm-ng tcpreplay
