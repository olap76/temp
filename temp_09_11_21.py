#!/usr/bin/python3

import sys
import re
import getpass
import json


from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# exec cli command on device and print output
def display_info(net_connect, cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

def dev_connect(pe):
  try:
    device = {
        "device_type": "juniper",
        "host": pe,
        "username": "o.laposhin",
        "password": password
        }

    net_connect = ConnectHandler(**device)


    with open('file_09_11_21.txt') as f:
        file = f.read().splitlines()


    for entry in file:

        cli_line = 'show configuration | display set | match ' + entry
#        cli_line = 'show configuration interfaces ' + entry

        output = net_connect.send_command(cli_line)

        print(output)


        # if 'show route ...' not empty 
#        if len(temp['route-information'][0]) > 1:
#            print(temp['route-information'][0])
            # get BPE interface
#            ae20_iface = temp['route-information'][0]['route-table'][0]['rt'][1]['rt-entry'][0]['nh'][0]['nh-local-interface'][0]['data']

#            cli_line = 'show interfaces descriptions ' + ae20_iface
#            output = net_connect.send_command(cli_line)
#            print(output)


    # close connection
    net_connect.disconnect()

  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print('<<<ERROR:>>>', router, error)

if __name__ == '__main__':

    # get pe
    pe = "185.64.44.11"
    # get password
    password = getpass.getpass()

    dev_connect(pe)

