#!/usr/bin/env bash

#how long does it take to transfer it? 10min
#how long did it took to develop this? 3 days

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

#sudo bash -c 'cat << EOF > /etc/nginx/sites-available/nftower.conf
#server {
#        listen 80;
#        server_name nftower.rockbio.io;
#
#        error_log /var/log/nginx/nftower.error;
#        access_log /var/log/nginx/nftower.access;
#        location / {
#                proxy_pass http://10.29.145.81:8000/;
#                proxy_set_header Host \$host;
#                proxy_set_header Upgrade \$http_upgrade;
#                proxy_set_header Connection upgrade;
#                proxy_set_header Accept-Encoding gzip;
#        }
#}
#EOF'
#
#sudo ln -s /etc/nginx/sites-available/nftower.conf /etc/nginx/sites-enabled/nftower.conf
#sudo service nginx restart
#sudo certbot --nginx --non-interactive --agree-tos -m raony@rockbio.io -d "nftower.rockbio.io"
#create nginx file with lxd ip and newdns
#
#sudo bash -c 'cat << EOF > /etc/nginx/sites-available/rockbio
#server {
#    listen 80;
#    location = /favicon.ico { access_log off; log_not_found off; }
#    location /static/ {
#        root /projects/rockbio/;
#    }
#
#    location / {
#        include proxy_params;
#        client_max_body_size 100G;
#        proxy_pass http://unix:/projects/rockbio/rockbio.sock;
#    }
#}
#EOF'

#add cert to new dns
#certbot
#restart nginx

#calculate end time
