#!/usr/bin/python3

import sys
import pexpect
import time

host_ip = sys.argv[1]

child = pexpect.spawn('telnet ' + host_ip)

#child.interact()

time.sleep(3)
child.sendline('c\n')
child.expect('User Name:')
child.sendline('c\r')
child.expect('Password:')
child.sendline('c\r')
child.expect('Select =>')
child.sendline('8\r')
child.expect('Select =>')
time.sleep(1)
child.sendline('1\r')
time.sleep(1)
child.sendline('admin\r')
time.sleep(1)
child.sendline('rhsv2014\r')
time.sleep(1)
child.sendline('rhsv2014\r')
time.sleep(1)
child.sendline('w\r')
time.sleep(1)
child.sendline('*.*.*.*\r')
time.sleep(1)

child.expect('Select =>')
time.sleep(1)
child.sendline('0\r')
time.sleep(1)

#child.interact()

child.expect('Select =>')
time.sleep(1)
child.sendline('c\r')
time.sleep(1)
child.expect('\?')
time.sleep(1)
child.sendline('y\r')
time.sleep(1)
child.close()
