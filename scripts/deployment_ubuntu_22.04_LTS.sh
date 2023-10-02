#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive
sudo apt update

sudo apt install -y nginx build-essential gcc git htop libbz2-dev libcurl4-openssl-dev libffi-dev \
liblzma-dev libssl-dev libxml2-dev make python3-lxml python3 python3-dev python3-venv python3-wheel \
sudo zip zlib1g zlib1g-dev rabbitmq-server

sudo mkdir /projects
cd /projects
sudo chown $USER .

git clone https://github.com/rockbio/rockbio
cd rockbio/

#set up database
sudo apt-get install -y libpq-dev postgresql
echo "create user $USER password ''; ALTER USER $USER WITH SUPERUSER;" > /tmp/create_user.sql
sudo -u postgres psql --file=/tmp/create_user.sql
createdb rockbio
cp rockbio/local_settings.sample.py rockbio/local_settings.py

python3 -m venv /projects/venv
source /projects/venv/bin/activate
pip install wheel
pip install -r requirements.txt

python manage.py migrate
python manage.py populate

#python manage.py createsuperuser
#python manage.py runserver

sudo bash -c 'cat << EOF > /etc/nginx/sites-available/rockbio
server {
    listen 80;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /projects/rockbio/;
    }

    location / {
        include proxy_params;
        client_max_body_size 100G;
        proxy_pass http://unix:/projects/rockbio/rockbio.sock;
    }
}
EOF'

sudo bash -c 'cat << EOF > /etc/systemd/system/rockbio.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/projects/rockbio/
ExecStart=/projects/venv/bin/gunicorn --access-logfile - --workers 4 --timeout 900 --bind unix:/projects/rockbio/rockbio.sock rockbio.wsgi:application

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable rockbio
sudo systemctl start rockbio
sudo ln -s /etc/nginx/sites-available/rockbio /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx reload
#add apache config

#add celery config

# sudo a2enmod proxy
# sudo a2enmod proxy_http
# sudo a2enmod proxy_balancer

# sudo service apache2 restart