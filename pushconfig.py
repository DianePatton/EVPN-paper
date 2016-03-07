#! /usr/bin/env python

import sys
import paramiko
from paramiko import SSHClient

try:
    demo = sys.argv[1]
    hostnames = sys.argv[2].split(',')
    url = "http://oob-mgmt-server.lab.local/cldemo-config/%s/"%demo
except:
    print("Usage: pushconfig [demo] [leaf01,leaf02,etc]")
    sys.exit(-1)

for host in hostnames:
    expect = paramiko.SSHClient()
    expect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    expect.connect(switch.name, username="cumulus", password="CumulusLinux!")
    stdin, stdout, stderr = expect.exec_command("sudo su", get_pty=True)
    stdin.write('CumulusLinux!\n')
    stdin.flush()
    stdin.write('wget %s/%s/interfaces\n'%(url, host))
    stdin.write('wget %s/%s/Quagga.conf\n'%(url, host))
    stdin.write('wget %s/%s/daemons\n'%(url, host))
    stdin.write('mv interfaces /etc/network/interfaces\n')
    stdin.write('mv Quagga.conf /etc/quagga/Quagga.conf\n')
    stdin.write('mv daemons /etc/quagga/daemons\n')
    stdin.write('reboot\n')
    stdin.flush()
    # Note, this printline is necessary in order for the aplication to run
    print(stderr.read())
    expect.close()
