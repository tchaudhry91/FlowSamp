sudo sed -i "s/\mirrors.kernel.org/old-releases.ubuntu.com/g" /etc/apt/sources.list
sudo sed -i -e 's/archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

sudo apt-get install bwm-ng tcpreplay
