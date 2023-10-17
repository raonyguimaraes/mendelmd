#!/usr/bin/env python3

from subprocess import check_output
import os
import argparse
import subprocess
import json
import os, sys
import gzip

#for cpanel
from re import compile
from http import client
from base64 import b64encode

script_dir = os.getcwd()
current_dir = os.getcwd().split('/')
#remove just one path and add mendel,md source

del current_dir[-1]
proj_path = "/".join(current_dir)
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rockbio.settings")
sys.path.append(script_dir)
sys.path.append(proj_path)


# This is so my local_settings.py gets loaded.
# os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from tasks.models import Task
from keys.models import CloudKey

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-i", "--task_id", help = "appname")

# Read arguments from command line
args = parser.parse_args()
print('args',args)
print('transfer app!') 

task=Task.objects.get(id=args.task_id)

print(task.manifest)

manifest=task.manifest

ip_origin=manifest['server_ip']
ip_dest=manifest['server_destination']
app_name=manifest['name']
new_dns=manifest['new_dns']

def run(command):
    print(command)
    subprocess.run(command,shell=True)

def run_remote(command):
    command = f'ssh -t root@{ip_dest} {command}'
    print(command)
    os.system(command)
    # subprocess.run(command,shell=True)

#
# command = f'ssh root@{ip_origin} tar -czvf galaxy.tar.gz galaxy/'
# run(command)
#
# print('transfer here')
# run(f'rsync -rtvh root@{ip_origin}:/root/galaxy.tar.gz work_dir/')
#
# print("Transfer to Destination")
# run(f'rsync -rtvh work_dir/galaxy.tar.gz root@{ip_dest}:/root/galaxy.tar.gz')

print('now install')
#now install there
run_remote(f'lxc delete {app_name} --force')
run_remote(f'lxc launch ubuntu:22.04 {app_name} -c security.nesting=true')
# run_remote(f'lxc config set {app_name} security.privileged true')
# run_remote(f'lxc config set {app_name} limits.cpu 2')
# run_remote(f'lxc config set {app_name} limits.memory 16GB')
# run_remote(f'lxc file push /root/{app_name}.tar.gz {app_name}/root/{app_name}.tar.gz')
# run_remote(f'lxc exec {app_name} -- tar -zxvf {app_name}.tar.gz')
# run_remote(f'lxc exec {app_name} -- apt update')
# run_remote(f'lxc exec {app_name} -- apt -y install python3-venv python3-pip')
# run_remote(f'lxc exec {app_name} -- snap install yq')
#
#
#
# run_remote(f'lxc exec {app_name} --cwd /root/galaxy -- rm -rf .venv')

subcommand = 'grep -qxF \'uvicorn[standard]\' requirements.txt || echo \'uvicorn[standard]\' >> requirements.txt'
command=f'lxc exec {app_name} --cwd /root/galaxy -- {subcommand}'
run_remote(command)
die()


command=f'lxc exec {app_name} --cwd /root/galaxy -- yq -i \'.gravity.gunicorn.bind=\\"0.0.0.0:8080\\"\' config/galaxy.yml'
run_remote(command)
run_remote(f'lxc exec {app_name} --cwd /root/galaxy -- sh run.sh &')

#update dns
data=task.manifest
manifest=task.manifest

print(data['new_dns'])

newdns = data['new_dns']
maindomain = '.'.join(newdns.split('.')[-2:])

cpanel = CloudKey.objects.get(cloudprovider="Cpanel")

conn = client.HTTPSConnection(cpanel.host, 2083)
binarystring = '{}:{}'.format(cpanel.username, cpanel.password).encode()
myAuth = b64encode(binarystring).decode('ascii')
authHeader = {'Authorization': 'Basic ' + myAuth}
conn.request('GET',
    '/json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=fetchzone_records&domain={}'.format(
        maindomain),
    headers=authHeader)

myResponse = conn.getresponse()
print(myResponse.getcode())
data = myResponse.read()
if myResponse.getcode() != 200:
    print('did not succeed')
# print(data)
data2 = json.loads(data)
line_number = None
for zone_record in data2['cpanelresult']['data']:
    # print(zone_record)
    if 'name' in zone_record:
        if zone_record['name'].startswith(newdns):
            # get line number and update
            line_number = str(zone_record['Line'])
            print('line number {}'.format(line_number))

newIP = manifest['server_destination']
print('new IP, ', newIP)
if line_number:
    # update record
    conn.request('GET',
                    '/json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=edit_zone_record&domain=' + maindomain + '&line=' + line_number + '&class=IN&type=A&name=' + newdns + '.&ttl=3600&address=' + newIP,
                    headers=authHeader)
else:
    # add record
    conn.request('GET',
                    '/json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=add_zone_record&domain=' + maindomain + '&class=IN&type=A&name=' + newdns + '.&ttl=3600&address=' + newIP,
                    headers=authHeader)
myResponse = conn.getresponse()
print(myResponse.getcode())

#install nginx
subcommand = 'lxc list galaxy --format=json'
command = f'ssh -t root@{ip_dest} {subcommand}'

output = check_output(command, shell=True)
outjson=json.loads(output.decode())

# print(outjson[0].keys())
# for lxc in outjson:
print('name',outjson[0]['name'])
# if lxc['name']=='nf-tower':
    # print(lxc.keys())
lxc_ip = outjson[0]['state']['network']['eth0']['addresses'][0]['address']
print(lxc_ip)

# new_dns=task.manifest['new_dns']
    #add nginx
subcommand = f'''sudo bash -c 'cat << EOF > /etc/nginx/sites-available/{app_name}.conf
server {{
    listen 80;
    server_name {new_dns};

    error_log /var/log/nginx/{app_name}.error;
    access_log /var/log/nginx/{app_name}.access;
    location / {{
            proxy_pass http://{lxc_ip}:8080/;
            proxy_set_header Host \$host;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection upgrade;
            proxy_set_header Accept-Encoding gzip;
    }}
}}
EOF' '''
run_remote(subcommand)

run_remote(f'sudo ln -sf /etc/nginx/sites-available/{app_name}.conf /etc/nginx/sites-enabled/{app_name}.conf')
run_remote('sudo service nginx restart')

subcommand = 'certbot --nginx --non-interactive --agree-tos -m raony@rockbio.io -d "{}"'.format(new_dns)
run_remote(subcommand)

# command = 'ssh -t root@{} {}'.format(
#     ip, subcommand)
# output = check_output(command, shell=True)

#lxc config set container_name limits.memory 16GB
#
#lxc file push nf-tower.tar.gz nf-tower/root/nf-tower.tar.gz
#lxc exec nf-tower -- sh -c "tar -zxvf nf-tower.tar.gz"


# rsync -rtvh scripts/install_nf-tower_lxd.sh root@$ip_dest:/root/

# echo "Install NF-Tower"
# ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$ip_dest bash install_nf-tower_lxd.sh

#ssh -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$ip_dest -- sh -c 'bash install_nf-tower_lxd.sh 2>&1'
#-q
# lxc delete nf-tower --force;lxc launch ubuntu:22.04 nf-tower -c security.nesting=true
# lxc config set nf-tower security.privileged true
# lxc config set nf-tower limits.cpu 2
# lxc config set container_name limits.memory 16GB

# lxc file push nf-tower.tar.gz nf-tower/root/nf-tower.tar.gz
# lxc exec nf-tower -- sh -c "tar -zxvf nf-tower.tar.gz"
# lxc exec nf-tower -- sh -c "sudo apt-get update;apt install -y make docker.io docker-compose"
# lxc exec nf-tower -- sh -c "sudo apt-get update;apt install -y openjdk-11-jdk"

# echo "Build..."
# lxc exec nf-tower -- sh -c "cd nf-tower;make build"
# lxc exec nf-tower -- sh -c "cd nf-tower;make run"

# echo "Finished"