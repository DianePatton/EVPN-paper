Demo Routing Configurations
===========================
Version: Cumulus Linux 2.5.6


Quickstart: Run the demo
------------------------
(This assumes you are running Ansible 1.9.4 and Vagrant 1.8.4 on your host.)

    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    vagrant up
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    git clone https://github.com/cumulusnetworks/cldemo-config-routing
    cd cldemo-config-routing
    sudo ln -s  /home/cumulus/cldemo-config-routing /var/www/cldemo-config-routing
    python pushconfig.py bgp-numbered leaf01,leaf02,spine01,spine02,server01,server02
    ssh server01
    ping 172.16.2.101


Description
-----------
This Github repository contains the configuration files necessary for setting
up Layer 3 routing on a CLOS topology using Cumulus Linux and Quagga. Eight
protocols are included:

 * OSPF Numbered
 * OSPF Unnumbered
 * BGP Numbered
 * BGP Unnumbered
 * OSPF Numbered with IPv6
 * OSPF Unnumbered with IPv6
 * BGP Numbered with IPv6
 * BGP Unnumbered with IPv6

To use this repository, copy the interfaces file to `/etc/network/` and the
Quagga.conf and daemons file to `/etc/quagga/` onto each device and reboot. A
helper script is provided to simplify this (this assumes you have a server
named oob-mgmt-server connected to all of your devices via eth0 that's running
apache or nginx). To use the helper script, create a symlink to the
cldemo-config-routing folder in `/var/www` on the oob-mgmt-server. Then run

    python pushconfig.py <demo_name> leaf01,leaf02,spine01,spine02,server01,server02,etc...


Topology
--------
                     +--------------+  +--------------+
                     | spine01      |  | spine02      |
                     |              |  |              |
                     +--------------+  +--------------+
                    swp1-4 ||||                |||| swp1-4
             +---------------------------------+|||
             |             ||||+----------------+|+----------------+
             |             |||+---------------------------------+  |
          +----------------+|+----------------+  |              |  |
    swp51 |  | swp52  swp51 |  | swp52  swp51 |  | swp52  swp51 |  | swp52
    +--------------+  +--------------+  +--------------+  +--------------+
    | leaf01       |  | leaf02       |  | leaf03       |  | leaf04       |
    |              |  |              |  |              |  |              |
    +--------------+  +--------------+  +--------------+  +--------------+
      swp1 |            swp2 |            swp1 |            swp2 |
           |                 |                 |                 |
      eth1 |            eth2 |            eth1 |            eth2 |
    +--------------+  +--------------+  +--------------+  +--------------+
    | server01     |  | server02     |  | server03     |  | server04     |
    |              |  |              |  |              |  |              |
    +--------------+  +--------------+  +--------------+  +--------------+

For a virtual topology, please follow the steps in [cldemo-vagrant](https://github.com/cumulusnetworks/cldemo-vagrant)


Syntax Checking
---------------
The syntax of all of the Quagga.conf files in this repository can be verified
using the following line in bash.

     for i in `find  | grep Quagga.conf`; do vtysh -f $i --dryrun; done ;
