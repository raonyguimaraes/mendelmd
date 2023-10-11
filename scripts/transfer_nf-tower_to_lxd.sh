#!/usr/bin/env bash

ip_origin=$1
ip_dest=$2
echo $ip_origin $ip_dest
echo "Transfer to LXD"
# sudo apt update
rsync -avz root@$ip_origin:/root/nf-tower.tar.gz .
rsync -avz nf-tower.tar.gz root@$ip_dest:/root/nf-tower.tar.gz
rsync -avz scripts/install_nf-tower_lxd.sh root@$ip_dest:/root/install_nf-tower_lxd.sh

echo "Install NF-Tower"
ssh -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$ip_dest -- sh -c 'cd nf-tower; bash install_nf-tower_lxd.sh'

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