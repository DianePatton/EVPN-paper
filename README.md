Demo Routing Configurations
===========================
This Github repository contains the configuration files necessary for setting up Layer 3 routing on a CLOS topology using Cumulus Linux and Quagga on the [Reference Topology](http://github.com/cumulusnetworks/cldemo-vagrant). Eight protocols are included:

 * OSPF Numbered
 * OSPF Unnumbered
 * BGP Numbered
 * BGP Unnumbered
 * OSPF Numbered with IPv6
 * OSPF Unnumbered with IPv6
 * BGP Numbered with IPv6
 * BGP Unnumbered with IPv6

The flatfiles in this repository will set up a Layer 3 routing fabric between the leafs and spines, and will configure a Layer 2 bridge on each leaf top-of-rack switch for the servers in that rack. Servers access other servers in the same rack with one hop across the leaf top-of-rack, and access servers in other racks via one of the spine switches. A helper script named `push-config.py` is available to quickly deploy the flatfiles to the devices in the network, but you could just as easily copy and paste them by hand or incorporate them into an automation tool instead.


Quickstart: Run the demo
------------------------
(This assumes you are running Ansible 1.9.4 and Vagrant 1.8.4 on your host.)

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02 spine01 spine02 server01 server02
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    git clone https://github.com/cumulusnetworks/cldemo-config-routing
    cd cldemo-config-routing
    sudo ln -s  /home/cumulus/cldemo-config-routing /var/www/cldemo-config-routing
    python pushconfig.py bgp-unnumbered leaf01,leaf02,spine01,spine02,server01,server02
    ssh server01
    ping 172.16.2.101


Topology
--------
This demo runs on a spine-leaf topology with two single-attached hosts. The helper script `push-config.py` requires an out-of-band management network that provides access to eth0 on all of the in-band devices.

         +------------+       +------------+
         | spine01    |       | spine02    |
         |            |       |            |
         +------------+       +------------+
         swp1 |    swp2 \   / swp1    | swp2
              |           X           |
        swp51 |   swp52 /   \ swp51   | swp52
         +------------+       +------------+
         | leaf01     |       | leaf02     |
         |            |       |            |
         +------------+       +------------+
         swp1 |                       | swp2
              |                       |
         eth1 |                       | eth2
         +------------+       +------------+
         | server01   |       | server02   |
         |            |       |            |
         +------------+       +------------+


Using the Helper Script
-----------------------
The `push-config.py` helper script deploys the configuration to the in-band network by downloading the files from the out-of-band management server. This requires a web server to be installed on the out-of-band server and passwordless login and sudo to be enabled on the in-band devices, both of which are done for you if you used [cldemo-vagrant](http://github.com/cumulusnetworks/cldemo-vagrant) to provision your topology. The demo repository needs to be linked in the management server's `/var/www/` directory:

    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    git clone https://github.com/cumulusnetworks/cldemo-config-routing
    cd cldemo-config-routing
    sudo ln -s  /home/cumulus/cldemo-config-routing /var/www/cldemo-config-routing

After setting up the repo, you can now use `push-config.py`! This script will log in to each device, download the files, and reboot the device.

    python pushconfig.py <demo_name> leaf01,leaf02,spine01,spine02,server01,server02


Verifying Routing
-----------------
Running the demo is easiest with two terminal windows open. One window will log into server01 and ping server02's IP address. The second window will be used to deploy new configuration on the switches.

*In terminal 1*

    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    cd cldemo-config-routing
    python pushconfig.py bgp-unnumbered leaf01,leaf02,spine01,spine02,server01,server02

*In terminal 2*

    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    ssh server01
    ping 172.16.2.101

*In terminal 1*

    python pushconfig.py ospf-unnumbered leaf01,leaf02,spine01,spine02
    # wait and watch connectivity drop and then come back
    python pushconfig.py bgp-numbered leaf01,leaf02,spine01,spine02
    # again
    python pushconfig.py bgp-unnumbered-ipv6 leaf01,leaf02,spine01,spine02,server01,server02
    # this will reboot server01, so you'll need to log back in in terminal 2


Verify High Availability
------------------------
Using a routing protocol such as BGP or OSPF means that as long as one spine is still running, the network will automatically learn a new route and keep the fabric connected. This means that you can do rolling upgrades one spine at a time without incurring any downtime.

*In terminal 1*

    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    cd cldemo-config-routing
    python pushconfig.py bgp-unnumbered leaf01,leaf02,spine01,spine02,server01,server02

*In terminal 2*

    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    ssh server01
    ping 172.16.2.101
    
*In terminal 3*

    vagrant destroy -f spine01
    # note that the pings may hiccup a bit, but will keep going
    vagrant destroy -f spine02
    # now pings will totally fail
    vagrant up spine01 spine02

*In terminal 1*

    python pushconfig.py bgp-unnumbered spine01,spine02
    # watch Terminal 2, and pings will return


Using Quagga Dry Runs for Syntax Checking
-----------------------------------------
You can use Quagga's dry run functionality to check the syntax of Quagga configuration without applying the changes.

    vtysh -f Quagga.conf --dryrun

The syntax of all of the Quagga.conf files in this repository can be verified using the following line in bash.

     for i in `find  | grep Quagga.conf`; do vtysh -f $i --dryrun; done ;
