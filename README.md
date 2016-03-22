Demo Routing Configurations
===========================
Version: Cumulus Linux 2.5.6


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
apache or nginx).

    cd /var/www
    sudo apt-get install python-paramiko
    git clone https://github.com/cumulusnetworks/cldemo-config-routing
    cd cldemo-config-routing
    python pushconfig.py bgp-numbered server01,server02,leaf01,leaf02,spine01,spine02


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


Syntax Checking
---------------
The syntax of all of the Quagga.conf files in this repository can be verified
using the following line in bash.

     for i in `find  | grep Quagga.conf`; do vtysh -f $i --dryrun; done ;
