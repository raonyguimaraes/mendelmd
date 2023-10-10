#!/usr/bin/python3
from subprocess import run,check_output
import os
command = 'mkdir /mnt/hd'
run(command,shell=True)

command = 'mount /dev/sda1 /mnt/hd'
run(command,shell=True)

#check if file exists, if not create it
#cat pub_key >> ~/.ssh/authorized_keys
authorized_key = open('/root/.ssh/authorized_keys','r').readlines()[0]
print(authorized_key)

path='/mnt/hd/root/.ssh/authorized_keys'
if os.path.isfile(path):
    with open(path, "r+") as file:
        for line in file:
            if authorized_key in line:
               break
        else: # not found, we are at the eof
            file.write(authorized_key) # append missing data
else:
    command = 'cp /root/.ssh/authorized_keys /mnt/hd/root/.ssh/authorized_keys'
    run(command,shell=True)