#!/usr/bin/env bash

echo "Restore Discourse!"
lxc storage delete docker
lxc storage create docker btrfs size=10GiB
lxc delete discourse --force;
lxc launch images:ubuntu/20.04 discourse

lxc storage volume create docker discourse
lxc config device add discourse docker disk pool=docker source=discourse path=/var/lib/docker
lxc config set discourse security.nesting=true security.syscalls.intercept.mknod=true security.syscalls.intercept.setxattr=true
lxc restart discourse

lxc exec discourse -- apt install -y docker git
lxc file push /root/rockbio-2023-10-20-190817-v20230926165821.tar.gz discourse/root/discoursebackup.tar.gz
lxc file push /root/app.yml discourse/root/app.yml

lxc exec discourse -- git clone https://github.com/discourse/discourse_docker.git /var/discourse
lxc exec discourse -- cp app.yml /var/discourse/containers
lxc exec discourse -- chmod 700 containers
lxc exec discourse -- sh -c "cd /var/discourse; ls"
