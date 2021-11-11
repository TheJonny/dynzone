#!/usr/bin/env python3

import ipaddress
from ipaddress import IPv6Address, ip_interface, IPv6Network
import json
import subprocess
import os

INTERFACE = "eth0"

out = subprocess.check_output(["ip", "-6", "-br", "-j", "addr", "show", "dev", INTERFACE])
j = json.loads(out)

addrs = [ip_interface(ai["local"]+"/"+str(ai["prefixlen"])) for ai in j[0]["addr_info"]]
addrs = [a for a in addrs if a.is_global]
my_networks = set([a.network for a in addrs])
if not my_networks:
    exit("no global addresses found")

keep = True

if not os.path.exists("current-ips"):
    print("file current-ips does not exist yet")
    keep=False
elif os.stat("current-ips").st_mtime < os.stat("suffixes").st_mtime:
    print("file suffixes is newer than current-ips")
    keep=False

with open("suffixes") as f:
    suffixes = [l.split() for l in f]

suffixes = [(name, IPv6Address(suffix)) for (name, suffix) in suffixes]
new_entries = [(name, IPv6Address(int(net.network_address) | int(suffix))) for (name, suffix) in suffixes for net in my_networks]

current_entries = []
if keep:
    with open("current-ips") as f:
        current_entries = [l.split() for l in f]
    current_entries = [(name, IPv6Address(addr)) for (name, _aaaa, addr) in current_entries]

if current_entries != new_entries:
    print("new file is different")
    keep = False


if keep:
    print("keeping")
    exit(0)

if not keep:
    with open("current-ips", "w") as f:
        for name, address in new_entries:
            print(name, "aaaa", address, file=f)
