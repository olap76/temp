#!/usr/bin/python3

import pexpect
import re
import time

username = 'o.laposhin'
password = 'Ureacoh9'

def parse_host(host):

    match_ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host)

    # if arg is IP address
    if match_ip:
        host = match_ip.group()
    else:
    # if arg is hostname
        match_domain = re.search('.net$', host)
        if not match_domain:
            host = host + ".miranda-media.net"

    return host

def telnet_to_host(child):

    child.expect('(User Name:)|(login:)|(Username:)')
    #child.expect('(User Name:)|(login:)')
    child.sendline(username)

    child.expect('Password:')
    child.sendline(password)

    child.expect('#')
    child.sendline('\n')

def cli_show_ver(child):

    child.expect('#')
    child.sendline('show ver\n')
    child.expect('#')
    print(child.before.decode('utf-8'))
#    child.expect('#')

# exit SSW
def logout(child):
    child.sendline('exit')

def cli_port_add(child, model, client_port, descr, vid, cl_port_type):

  if cl_port_type == 'a':
    if (model == '1' or model == '2'):
      child.sendline('conf\n')
      time.sleep(1)
      child.sendline('interface ' + client_port + '\n')

      child.sendline('description \"' + descr + '\"\n')
      child.sendline('loopback-detection enable\n')
      child.sendline('storm-control broadcast kbps 103 shutdown\n')
      time.sleep(1)
      child.sendline('switchport protected-port\n')
      child.sendline('switchport access vlan ' + vid + '\n')
      time.sleep(1)
      child.sendline('switchport forbidden default-vlan\n')

      child.sendline('exit\n')
      child.sendline('exit\n')

    elif (model == '3'):
      child.sendline('conf\n')
      child.sendline('interface ' + client_port + '\n')

      child.sendline('description \"' + descr + '\"\n')
      child.sendline('bridge-protocol filter\n')
      child.sendline('storm-control brmc 512\n')
      child.sendline('transceiver-monitoring enable\n')
      child.sendline('lldp disable\n')
      child.sendline('switchport mode access\n')
      child.sendline('switchport access vlan ' + vid + '\n')
      child.sendline('no loopback-detection specified-vlan\n')
      child.sendline('loopback-detection specified-vlan' + vid + '\n')
      child.sendline('loopback-detection control shutdown\n')

      child.sendline('exit\n')
      child.sendline('exit\n')

  elif cl_port_type == 't':
    if (model == '1' or model == '2'):
      child.sendline('conf\n')
      time.sleep(1)
      child.sendline('interface ' + client_port + '\n')

      child.sendline('switchport trunk allowed vlan add ' + vid + '\n')
#      child.interact()

      child.sendline('exit\n')
      child.sendline('exit\n')

    elif (model == '3'):
      print("cli_port_add, cl_port_type == 't', model == '3' - NOT IMPLEMENTED")

def cli_port_del(child, client_port):

    if client_port:
        child.sendline('conf\n')
        time.sleep(1)
        child.sendline('interface ' + client_port + '\n')
        child.sendline('no description\n')
        child.sendline('no loopback-detection enable\n')
        child.sendline('no storm-control broadcast\n')
        time.sleep(1)

        child.sendline('no switchport protected-port\n')
        child.sendline('no switchport access vlan\n')
        child.sendline('no switchport forbidden default-vlan\n')
        child.sendline('exit\n')
        child.sendline('exit\n')

def cli_vlan_add(child, model, vid, vlan_name):

    child.sendline('conf\n')

    if (model == '1'):
        child.sendline('vlan ' + vid + ' name ' + '\"' + vlan_name + '\"\n')

    elif (model == '2'):
        time.sleep(1)
        child.sendline('vlan database\n')
        child.sendline('vlan ' + vid + ' name ' + '\"' + vlan_name + '\"\n')
        child.sendline('exit\n')

    elif (model == '3'):
        time.sleep(1)
        child.sendline('vlan ' + vid + '\n')
        child.sendline('name ' + '\"' + vlan_name + '\"\n')
        child.sendline('exit\n')

    child.sendline('exit\n')

def cli_vlan_del(child, model, vid):

    child.sendline('conf\n')

    if (model == '1' or model == '3'):
        child.sendline('no vlan ' + vid + '\n')

    if (model == '2'):
        time.sleep(1)
        child.sendline('vlan database\n')
        child.sendline('no vlan ' + vid + '\n')
        child.sendline('exit\n')

    child.sendline('exit\n')

def cli_vlan_trunk_add(child, vid, trunk_port):

    child.sendline('conf\n')
    time.sleep(1)
    child.sendline('interface ' + trunk_port + '\n')
    time.sleep(1)
    child.sendline('switchport trunk allowed vlan add ' + vid + '\n')
    child.sendline('exit\n')
    child.sendline('exit\n')

def cli_vlan_trunk_del(child, vid, trunk_port):
    child.sendline('conf\n')
    time.sleep(1)
    child.sendline('interface ' + trunk_port + '\n')

    child.sendline('switchport trunk allowed vlan remove ' + vid + '\n')

    child.sendline('exit\n')
    child.sendline('exit\n')


def add_conf(child, host, model, client_port, vid, vlan_name, descr, cl_port_type):
    """ Add full config to SSW """

    cli_vlan_add(child, model, vid, vlan_name)
    cli_port_add(child, model, client_port, descr, vid, cl_port_type)
    cli_vlan_trunk_add(child, vid, trunk_port)


def del_conf(child, host, model, client_port, vid, cl_port_type):
    """ Delete full config from SSW """

    cli_port_del(child, client_port)
    cli_vlan_trunk_del(child, vid, trunk_port)
    cli_vlan_del(child, model,vid)

    #child.interact()

#------------- main script ------------------

# choose add or delete config
while True:
    user_select = input("Add or delete config (1 - ADD, 2 - DELETE)?: ")
    if (user_select == '1' or user_select == '2'):
        break

#get switch host or ip
host = input("Enter SSW hostname or ip: ")
#select SSW model
while True:
    model = input("Select SSW model (1 - eltex 33xx, 2 - eltex 11xx/31xx, 3 - qtech): ")
    if (model == '1' or model == '2' or model == '3'):
        break

#get empty SSW port
client_port = input("Enter client port: ")

if client_port:
  while True:
    cl_port_type = input("Client port type (a - ACCESS / t - trunk): ")
    if cl_port_type == 'a' or cl_port_type == 't':
      break

#get trunk port
trunk_port = input("Enter uplink (trunk) port: ")
#get vlan-id
vid = input("Enter vlan id: ")
#additional params for add conf
if (user_select == '1'):
    #get vlan name
    vlan_name = input("Enter vlan name: ")
    #get port descript
    descr = input("Enter port descr: ")

# link to telnet
t_link = 'telnet ' + parse_host(host)
# telnet
child = pexpect.spawn(t_link)
# login
telnet_to_host(child)
# add or delete conf
if user_select == '1':
    add_conf(child, host, model, client_port, vid, vlan_name, descr, cl_port_type)
else:
    del_conf(child, host, model, client_port, vid, cl_port_type)


# exit SSW
logout(child)

# fot test: 172.18.2.2 gi3/0/44
print('!!! CONFIG NOT SAVED !!!')
