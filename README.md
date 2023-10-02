# Rockbio cloud based tools for development, personalized medicine, data science and genome analysis.

![Build Status](https://travis-ci.org/rockbio/rockbio.svg?branch=master)
[![BSD License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Read The Docs](https://readthedocs.org/projects/rockbio/badge/?version=latest)](http://rockbio.readthedocs.io/en/latest/)
[![Django](https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif)](https://www.djangoproject.com)

This is an online tool developed to help doctors and scientists to analyse NGS data and identify disease causing variants using WES and WGS sequencing data from patients with Mendelian Disorders.

Rockbio is based on Mendel,MD:

http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005520

https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-16-S8-A2

https://www.genomeweb.com/informatics/software-tool-aims-easy-quick-mendelian-disease-diagnoses-genome-data

But it's got a lot more to it now, so try our servers on https://rockbio.io

Installation/Development
========================

    git clone https://github.com/rockbio/rockbio/
    cd rockbio/
    docker-compose up

Or using python3, virtualenv and pip: 

    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 manage.py migrate
    python3 manage.py populate
    python3 manage.py runserver

    #Then on another window for running the background tasks with Celery
    source venv/bin/activate
    ./manage.py celery    


Installation with Curl (to-do)
==============================

    curl -Sf https://install.rockbio.io | bash

# Installation using Docker
    git clone https://github.com/rockbio/rockbio
    cd rockbio
    docker-compose up

# Installation with pip (to-do)
    pip3 install rockbio
    rockbio runserver

# Installation with conda (to-do)
    conda install -c conda-forge rockbio
    rockbio runserver

# Using Dockerhub (to-do)
    docker run rockbio/rockbio

# Using SNAPs
    sudo snap install code --classic

# Using APT
    sudo apt install rockbio