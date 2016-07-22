Installation
============

Requirements
************

* Python 3.5
* Java 1.8
* Ubuntu LTS 16.04

Other Softwares Needed
**********************

* pynnotator

Quick Install in Ubuntu 14.04
*****************************

.. git clone https://raonyguimaraes@bitbucket.org/raonyguimaraes/mendelmd
.. cd mendelmd
.. sudo apt-get install python-pip python-dev
.. sudo pip install virtualenvwrapper
.. source virtualenvwrapper.sh
.. mkvirtualenv mendelmd
.. pip install -r requirements.txt
.. python manage.py syncdb
.. python manage.py runserver

Populating database
*******************

OMIM Data
*********

Register an access to the FTP site of omim: http://omim.org/downloads and download a file named "morbidmap" :

You will need to manually download a copy of this file from OMIM to the folder: mendelmd_source/data/omim  !


1) Installation of PosgreSQL Database
************************************************

.. code-block:: bash

   sudo apt-get install tasksel libpq-dev postgresql
   sudo tasksel

Select the following options: 

* Basic Ubuntu Server
* LAMP Server
* PostgreSQL database

Now you can create a database called "mendelmd" in PostgreSQL with the following commands:

.. code-block:: bash

   sudo su
   su postgres
   psql template1
   CREATE USER mendelmd WITH PASSWORD 'yourpassword';
   CREATE DATABASE mendelmd;
   GRANT ALL PRIVILEGES ON DATABASE mendelmd to mendelmd;
   \q


For Installation On Ubuntu 12.04/14.04 with Python 2.7
******************************************************

.. code-block:: bash

   sudo apt-get install python-pip virtualenvwrapper python-dev memcached libmemcached-dev tabix


Installation of Mendel,MD in a Virtual Enviroment
*************************************************

.. code-block:: bash

   #install and create a virtual enviroment
   sudo pip install virtualenvwrapper
   source virtualenvwrapper.sh
   mkvirtualenv mendelmd

   #clone the repository
   git clone https://raonyguimaraes@bitbucket.org/raonyguimaraes/mendelmd_master
   cd mendelmd_master
   #install numpy first
   easy_install numpy
   #install all the requirements (go to take a cup of coffee)
   pip install -r requirements.txt
   #create tables in database and migrate
   python manage.py syncdb --migrate

   #create a static folder in your webserver
   sudo mkdir /var/www/mendelmd_static
   sudo chown www-data:www-data /var/www/mendelmd_static/
   sudo chmod 775 /var/www/mendelmd_static/
   #copy media files to /var/www/mendelmd_static/
   python manage.py collectstatic
   #now you can create the administrator user
   python manage.py createsuperuser

   #and now we can finally start the server 
   python manage.py runserver


Installing the Annotator
************************

In order to filter the variants using the web interface of Mendel,MD you first need to annotate your VCF File using a pipeline developed together with this tool.

To install our annotator all you have to type is:
./mendelmd install

Running the Annotator
*********************

Mendel,MD comes with an annotator pipeline that integrates the most common annotators available: SNPEFF, SNPSIFT, VARIANT EFFECT PREDICTOR.
After uploading your VCF to the system you can run the annotation pipeline with the following command:

.. code-block:: bash

   python manage.py celeryd

This scheduler should start annotating all you uploaded VCFs. The full annotation pipeline should take around 40 minutes per VCF exome file.

PostgreSQL Database
*******************

sudo apt-get install postgresql

Create a database names mendelmd

CREATE DATABASE mendelmd;

