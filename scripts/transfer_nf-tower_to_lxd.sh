#!/usr/bin/env bash

ip_origin=$1
ip_dest=$2
echo $ip_origin $ip_dest
echo "Transfer to LXD"
# sudo apt update
rsync -rtvh root@$ip_origin:/root/nf-tower.tar.gz .
echo "Transfer to Destination"
rsync -rtvh nf-tower.tar.gz root@$ip_dest:/root/nf-tower.tar.gz
rsync -rtvh scripts/install_nf-tower_lxd.sh root@$ip_dest:/root/

echo "Install NF-Tower"
ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$ip_dest bash install_nf-tower_lxd.sh

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

echo "Finished"