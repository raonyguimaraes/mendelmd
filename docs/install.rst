Install
=========

Requirements
============

* Python 2.7.3

Dependencies
============

Django Tables 2
BeautifulSoup
goatools
numpy
fisher
django-celery
wikitools
SOAPpy
Fabric
django-sorting


Other Softwares
***************

* Genome Analysis Toolkit 2.6-5
* VEP 
* vcftools 0.1.10
* tabix
* Snpeff
* Snpsift

Installation on Ubuntu 14.04 LTS / Linux Mint 17.1
==================================================

git clone https://raonyguimaraes@bitbucket.org/raonyguimaraes/mendelmd_master
cd mendelmd_master
   
mkvirtualenv -p /usr/bin/python3 mendelmd
cd mendelmd_source
pip install Fabric3
fab install

Installing the Pynnotator
========================

pip install cython
pip install pynnotator
pynnotator install

Installing Mendel,MD
====================

cd mendelmd_source
pip install -r requirements.stable.txt

python manage.py migrate auth
python manage.py migrate
python manage.py populate
python manage.py runserver


And now you should have Mendel,MD running on address http://127.0.0.1:8000/

Creating super user
===================

python manage.py createsuperuser

Importing Data
==============

python manage.py populate

Upload your VCFs using the web interface
========================================




Start the annotation
====================

python manage.py celery worker