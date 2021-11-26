#!/usr/bin/python3

import sys
import pexpect
import re
import getpass

username = 'o.laposhin'
password = getpass.getpass()

host_list = [
'172.21.0.130',
'172.19.3.2',
'172.22.0.130',
'172.25.2.2',
'172.24.10.130',
'172.24.8.2',
'172.24.9.2',
'172.18.4.2',
'172.24.11.130',
'172.24.8.130',
'172.27.27.130',
            ]

for host in host_list:

  t_link = 'telnet ' + host

  child = pexpect.spawn(t_link)

  child.expect('(User Name:)|(login:)|(Username:)')
  #child.expect('(User Name:)|(login:)')
  child.sendline(username)

  child.expect('Password:')
  child.sendline(password)

  child.expect('#')
  child.sendline('show ver\n')
  child.expect('#')

  print(child.before.decode('utf-8'))
  child.close()
