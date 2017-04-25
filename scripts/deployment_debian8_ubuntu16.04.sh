sudo apt update

sudo apt install apache2 build-essential gcc git libapache2-mod-proxy-html libbz2-dev libffi-dev libssl-dev libxml2-dev make python-dev python-lxml python3 python3-dev python3-venv sudo virtualenvwrapper zip zlib1g zlib1g-dev zlibc liblzma-dev

sudo mkdir /projects
cd /projects
sudo chown $USER .
git clone https://github.com/raonyguimaraes/mendelmd
cd mendelmd/mendelmd_source/

sudo apt-get install libpq-dev postgresql
sudo -i -u postgres
createuser --interactive
exit
createdb mendelmd
cp mendelmd/local_settings.sample.py mendelmd/local_settings.py

python3 -m venv mendelmdenv
source mendelmdenv/bin/activate
pip install cython
pip install pysam
pip install -r requirements.txt
pynnotator install

python manage.py migrate
python manage.py populate
python manage.py createsuperuser
python manage.py runserver

sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_ajp
sudo a2enmod rewrite
sudo a2enmod deflate
sudo a2enmod headers
sudo a2enmod proxy_balancer
sudo a2enmod proxy_connect
sudo a2enmod proxy_html
sudo service apache2 restart
