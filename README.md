Demo Quagga Configurations
==========================
Version: Cumulus Linux 2.5.5


Description
-----------
This Github repository contains the configuration files necessary for setting
up Layer 3 routing on a CLOS topology using Cumulus Linux and Quagga. Four
protocols are included:

 * OSPF Numbered
 * OSPF Unnumbered
 * BGP Numbered
 * BGP Unnumbered

To use this repository, copy the interfaces file to `/etc/network/` and the
Quagga.conf and daemons file to `/etc/quagga/` on each device and reboot. A
helper script is provided to simplify this:

    cd /var/www
    git clone https://github.com/cumulusnetworks/cldemo-config
    python pushconfig.py bgp-unnumbered server01,server02,leaf01,leaf02,spine01,spine02


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


Caveats
-------
 * IPv6 fails on servers with older kernels due to lacking optimistic DAD.
   Disable DAD on eth1 and eth2 on the servers.
   `sudo sysctl net.ipv6.conf.eth1.accept_dad=0`
