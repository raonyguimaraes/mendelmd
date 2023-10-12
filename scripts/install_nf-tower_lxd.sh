#!/usr/bin/env bash

#how long does it take to transfer it?
#how long did it took to develop this?

#calculate start time
echo "Install NF-Tower"

#lxc delete nf-tower --force;lxc launch ubuntu:22.04 nf-tower -c security.nesting=true
#lxc config set nf-tower security.privileged true
#lxc config set nf-tower limits.cpu 2
#lxc config set container_name limits.memory 16GB
#
#lxc file push nf-tower.tar.gz nf-tower/root/nf-tower.tar.gz
#lxc exec nf-tower -- sh -c "tar -zxvf nf-tower.tar.gz"
#lxc exec nf-tower -- sh -c "sudo apt-get update;apt install -y make docker.io docker-compose"
#lxc exec nf-tower -- sh -c "sudo apt-get update;apt install -y openjdk-8-jdk"
#
## echo "Build..."
#lxc exec nf-tower -- sh -c "cd nf-tower;make build"
lxc exec nf-tower -- sh -c "cd nf-tower;docker-compose up -d"

#transfer domain using cpanel

#python change_dns.py dns ip

#create nginx file with lxd ip and newdns

#add cert to new dns

#restart nginx

#calculate end time
