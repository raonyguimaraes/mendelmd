export DEBIAN_FRONTEND=noninteractive
apt install -y -o Dpkg::Options::=--force-confnew sudo

sudo apt update

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

sudo locale-gen en_US.UTF-8

sudo apt install -y nginx build-essential gcc git htop libbz2-dev libcurl4-openssl-dev libffi-dev \
liblzma-dev libssl-dev libxml2-dev make python-dev python-lxml python3 python3-dev python3-venv python3-wheel \
sudo zip zlib1g zlib1g-dev zlibc rabbitmq-server

sudo mkdir /projects
cd /projects
sudo chown $USER .

git clone https://github.com/raonyguimaraes/rockbio
cd rockbio/
#git checkout development

#set up database
sudo apt-get install -y libpq-dev postgresql
echo "create user \"$USER\" password ''; CREATE ROLE \"$USER\" superuser; alter user \"$USER\" with createdb; ALTER ROLE \"$USER\" WITH LOGIN;" > /tmp/create_user.sql
sudo -u postgres psql --file=/tmp/create_user.sql
createdb rockbio
cp rockbio/local_settings.sample.py rockbio/local_settings.py

python3 -m venv /projects/venv
source /projects/venv/bin/activate
pip install wheel
pip install -r requirements.txt
#pynnotator install

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

bash -c 'cat << EOF > /tmp/rockbio.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/projects/rockbio/
ExecStart=/projects/venv/bin/gunicorn --access-logfile - --workers 4 --timeout 900 --bind unix:/projects/rockbio/rockbio.sock rockbio.wsgi:application

[Install]
WantedBy=multi-user.target
EOF'
sudo cp /tmp/rockbio.service /etc/systemd/system/rockbio.service

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
