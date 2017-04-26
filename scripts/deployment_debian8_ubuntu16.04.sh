sudo apt update

sudo apt install -y apache2 build-essential gcc git apache2-bin libbz2-dev libffi-dev libssl-dev \
libxml2-dev make python-dev python-lxml python3 python3-dev python3-venv python3-wheel sudo virtualenvwrapper zip zlib1g \
zlib1g-dev zlibc liblzma-dev libcurl4-openssl-dev htop


sudo chown $USER .

git clone https://github.com/raonyguimaraes/mendelmd
cd mendelmd/mendelmd_source/
#git checkout development

sudo apt-get install -y libpq-dev postgresql
echo "create user $USER password ''; ALTER USER $USER WITH SUPERUSER;" > /tmp/create_user.sql
sudo -u postgres psql --file=/tmp/create_user.sql
createdb mendelmd
cp mendelmd/local_settings.sample.py mendelmd/local_settings.py

python3 -m venv mendelmdenv
source mendelmdenv/bin/activate
pip install wheel
pip install -r requirements.txt
pynnotator install

python manage.py migrate
python manage.py populate
#python manage.py createsuperuser
#python manage.py runserver

#add apache config

#add celery config

sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer

sudo service apache2 restart
