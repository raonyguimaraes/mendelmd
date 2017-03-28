Mendel,MD
=========

An online tool for annotating, filtering and diagnosing Humans (Exome
and Genome) with Mendelian Disorders.

Requirements
============

-  Python 3.4+
-  Perl 5.8+
-  Java 1.8
-  Ubuntu LTS 16.04

Other Libraries Needed
======================

-  `pynnotator <https://github.com/raonyguimaraes/pynnotator>`__

OMIM Data
=========

You need to register an account at OMIM: http://omim.org/downloads and
submit a download request to get a file named "morbidmap".

After obtaining this file you need to put it inside this folder:
"mendelmd\_source/data/omim/".


Docker
======

Now it's possible to install and run Mendel,MD with a single command:

::

    docker-compose up

This command will create a container, download all the required tools and datasets and run the webserver.

This should take a few hours to complete for the first time.

Manual Installation
===================


Installing PostgreSQL Database
==============================

::

    sudo apt-get install libpq-dev postgresql
    sudo su
    su postgres
    psql template1
    CREATE USER mendelmd WITH PASSWORD 'mendelmd';
    CREATE DATABASE mendelmd;
    GRANT ALL PRIVILEGES ON DATABASE mendelmd to mendelmd;
    \q


Installation on Ubuntu 16.04 LTS (tested)
=========================================

::

    git clone https://github.com/raonyguimaraes/mendelmd.git
    cd mendelmd_master/mendelmd_source
    mkvirtualenv -p /usr/bin/python3 mendelmd

Installing the Pynnotator
=========================

::

    pip install cython
    pip install pynnotator
    pynnotator install

This will take a long time since it will download around 26GB of data.
Go grab a coffee and read a paper.

Installing Mendel,MD
====================

::

    pip install -r requirements.stable.txt

    python manage.py migrate auth
    python manage.py migrate
    python manage.py runserver

And now you should have Mendel,MD running on address
http://127.0.0.1:8000/

Creating a superuser
====================

::

    python manage.py createsuperuser

Importing Data
==============

::

    python manage.py populate

Upload your VCFs using the web interface
========================================

Start the annotation
====================

::

    python manage.py celery worker

Installation on RedHat/CentOS 7
===============================

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7
https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7


sudo yum update
sudo yum upgrade

wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum -y install epel-release-latest-7.noarch.rpm

sudo yum -y install python-pip httpd mod_wsgi git postgresql-devel gcc htop zlib-devel vim
sudo yum install httpd-devel
sudo systemctl start httpd
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum install -y python35u python35u-pip
sudo yum -y install python35u-devel
sudo pip3.5 install virtualenv
virtualenv mendelmdenv
source mendelmdenv/bin/activate
git clone https://github.com/raonyguimaraes/mendelmd
cd mendelmd/mendelmd_source/
pip install -r requirements.stable.txt 

vim mendelmd/local_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mendelprod',
        'USER': 'root',
        'PASSWORD': 'changeme',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

cd data/omim

wget https://data.omim.org/downloads/changeme/morbidmap.txt


python manage.py migrate auth

#ignore the following error: django.db.utils.ProgrammingError: relation "django_site" does not exist

python manage.py migrate
python manage.py populate
python manage.py createsuperuser
python manage.py runserver


sudo nano /etc/httpd/conf.d/django.conf


Alias /static /home/ec2-user/mendelmd/static
<Directory /home/ec2-user/mendelmd/static>
    Require all granted
</Directory>

<Directory /home/ec2-user/mendelmd/biocloud>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

WSGIDaemonProcess mendelmd python-path=/home/ec2-user/mendelmd:/home/ec2-user/mendelmdenv/lib/python3.5/site-packages
WSGIProcessGroup mendelmd
WSGIScriptAlias / /home/ec2-user/mendelmd/mendelmd/wsgi.py

sudo usermod -a -G ec2-user apache
chmod 710 /home/ec2-user
sudo chown :apache ~/mendelmd
sudo systemctl restart httpd
sudo systemctl enable httpd

Install modwsgi for python 3

https://github.com/GrahamDumpleton/mod_wsgi.git

#as root

wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.15.zip
unzip 4.5.15.zip
cd ./mod_wsgi-4.5.15
./configure --with-python=/bin/python3.5
make
make install

sudo service httpd restart
