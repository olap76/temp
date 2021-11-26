#!/usr/bin/python3

import getpass
from jnpr.junos import Device
from pprint import pprint

host = None
uname = None
pw = None

if host == None:
  host = input("Hostname or IP: ")
if uname == None:
  uname = input("Username: ")
if pw == None:
  pw = getpass.getpass()

dev = Device(host=host,user=uname,password=pw)
#dev = Device(host=host)

dev.open()
#print(dev.connected)
#print(dev.user)
pprint(dev.facts['hostname'])
pprint(dev.facts)
dev.close()
#print(dev.connected)
