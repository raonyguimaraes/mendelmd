Mendel,MD
=========

An online tool for organizing, annotating, filtering and diagnosing patients with Mendelian Disorders using Exome and Genome sequencing data.

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
    cd mendelmd/mendelmd_source
    

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

