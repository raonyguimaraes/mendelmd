sudo yum update
sudo yum upgrade

wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum -y install epel-release-latest-7.noarch.rpm

sudo yum -y install python-pip httpd mod_wsgi git postgresql-devel gcc htop zlib-devel vim screen httpd-devel

wget -qO- https://get.docker.com/ | sh
sudo usermod -aG docker $(whoami)
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo yum install -y epel-release
sudo yum install -y python-pip
sudo yum upgrade -y python*
sudo pip install docker-compose --force --upgrade

sudo mkdir /projects
cd /projects
sudo chown ec2-user .
git clone https://github.com/raonyguimaraes/mendelmd
cd mendelmd/mendelmd_source/
cp /tmp/morbidmap.txt data/omim/
docker-compose build
# docker-compose up -d
# docker-compose down

sudo bash -c 'cat << EOF > /etc/systemd/system/mendelmd.service
[Unit]
Description=Mendelmd
After=network.target docker.service
[Service]
Type=simple
WorkingDirectory=/projects/mendelmd/mendelmd_source
ExecStart=/usr/bin/docker-compose -f docker-compose.yml up
ExecStop=/usr/bin/docker-compose -f docker-compose.yml down
Restart=always
[Install]
WantedBy=multi-user.target
EOF'

sudo bash -c 'cat << EOF > /etc/httpd/conf.d/mendelmd.conf
<VirtualHost *:80>
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
EOF'

sudo /usr/sbin/setsebool -P httpd_can_network_connect 1

sudo systemctl enable mendelmd
sudo systemctl start mendelmd
sudo systemctl restart mendelmd

sudo systemctl enable httpd
sudo systemctl restart httpd
