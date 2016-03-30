#! /usr/bin/env python

# This script installs pushes our configuration to the target hosts.
# This script assumes that the 'cumulus' user has passwordless sudo enabled on
# the target devices, and that the cldemo has been installed as per the README.

import sys
import paramiko
import time
from paramiko import SSHClient
from multiprocessing import Process

def go(host, demo):
    url = "http://oob-mgmt-server.lab.local/cldemo-config-routing/%s/"%demo
    expect = paramiko.SSHClient()
    expect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    expect.connect(host, username="cumulus", password="CumulusLinux!")
    for line in ['sudo wget %s/%s/interfaces'%(url, host),
                 'sudo wget %s/%s/Quagga.conf'%(url, host),
                 'sudo wget %s/%s/daemons'%(url, host),
                 'sudo mv interfaces /etc/network/interfaces',
                 'sudo mv Quagga.conf /etc/quagga/Quagga.conf',
                 'sudo mv daemons /etc/quagga/daemons',
                 'sudo reboot']:
        stdin, stdout, stderr = expect.exec_command(line, get_pty=True)
        stdout.channel.recv_exit_status()
        print("%s: %s"%(host, line))
    expect.close()


if __name__ == "__main__":
    try:
        demo = sys.argv[1]
        hostnames = sys.argv[2].split(',')
    except:
        print("Usage: pushconfig.py [demo] [leaf01,leaf02,etc]")
        sys.exit(-1)

    processes = []
    for host in hostnames:
        p = Process(target=go, args=(host, demo))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
