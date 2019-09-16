Mendel,MD
=========

An online tool for organizing, annotating, filtering and diagnosing patients with Mendelian Disorders using Whole Exome or Genome sequencing data.

Requirements
============

-  Python 2.7 or 3.6+
-  Perl 5+
-  Java 1.7+

Other Libraries Needed
======================

-  `pynnotator <https://github.com/raonyguimaraes/pynnotator>`__

OMIM Data
=========

You will need to register an account in OMIM: http://omim.org/downloads and
submit a download request to get a file named "morbidmap".

After obtaining this file you need to put it inside this folder:
"data/omim/".

Docker
======

Now it's possible to install and run Mendel,MD with a single command:

::

    docker-compose up

This command will create a container, download all the required tools, datasets and run the webserver.

This should take a few hours to complete for the first time.

Manual Installation
===================

Installing PostgreSQL Database
==============================

::

    sudo apt-get install libpq-dev postgresql
    sudo -i -u postgres
    createuser --interactive
    exit
    createdb mendelmd
    cp mendelmd/local_settings.sample.py mendelmd/local_settings.py

Installation on Ubuntu 16.04 LTS (tested)
=========================================

::

    sudo apt-get install gcc git python3-dev virtualenvwrapper zip zlibc zlib1g zlib1g-dev build-essential \
    libssl-dev libffi-dev python-dev python3-dev python3-venv libcurl4-openssl-dev

    python3 -m venv mendelmdenv
    source mendelmdenv/bin/activate

    git clone https://github.com/raonyguimaraes/mendelmd.git
    cd mendelmd/


Installing Pynnotator
=====================

::

    pip install wheel
    pip install pynnotator
    pynnotator install

This will take a long time since it will download around 32GB of data.
Go grab a coffee and read a paper.

Installing Mendel,MD
====================

::

    pip install -r requirements.txt

    python manage.py migrate

    wget https://data.omim.org/downloads/ADDYOURKEY/morbidmap.txt -O data/omim/morbidmap.txt
    python manage.py populate

    #create yourself a super user
    python manage.py createsuperuser

    python manage.py runserver

And now you should have Mendel,MD running on address
http://127.0.0.1:8000/


Start the annotation
====================

In another tab start the annotation process.

::

    source mendelmdenv/bin/activate
    celery -A mendelmd worker -l info -c 1



Creating a superuser
====================

::

    python manage.py createsuperuser

Importing Genes and Diseases Data
=================================

::

    python manage.py populate

Upload your VCFs using the web interface
========================================

At the dashboard click on the "Upload VCF" button.

Deployment on RedHat/CentOS 7
===============================

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7

::

    sudo yum -y install wget
    wget https://data.omim.org/downloads/ADDYOURKEY/morbidmap.txt -O /tmp/morbidmap.txt
    wget https://raw.github.com/raonyguimaraes/mendelmd/master/scripts/deployment_centos7_redhat7.sh
    bash deployment_centos7_redhat7.sh


Celery in Production
====================
https://github.com/celery/celery/blob/3.1/extra/generic-init.d/celeryd

# cat celeryd
# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/projects/mendelmdenv/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="mendelmd"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYD_CHDIR="/projects/mendelmd/"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=2 -Q annotation,insertion"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
#CELERYD_LOG_LEVEL="DEBUG"

# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).
CELERYD_USER="ubuntu"
CELERYD_GROUP="www-data"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1

