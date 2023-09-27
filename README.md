# Rockbio online tools for development, personalized medicine, data science and genome analysis.

![Build Status](https://travis-ci.org/raonyguimaraes/mendelmd.svg?branch=master)
[![BSD License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Read The Docs](https://readthedocs.org/projects/mendelmd/badge/?version=latest)](http://mendelmd.readthedocs.io/en/latest/)
[![Django](https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif)](https://www.djangoproject.com)

This is an online tool created to help doctors and scientists to identify disease causing variants using exome/genome sequencing data from patients with mendelian disorders.

Recently added M-CAP scores, filtering for CADD scores and Haploinsufficiency Scores.

http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005520

https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-16-S8-A2

Try our new test server on https://rockbio.io

Installation of docker and docker-compose on Ubuntu 16.04 LTS
=============================================================

    sudo apt-get update
    sudo apt-get install software-properties-common apt-transport-https libffi-dev
    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
    sudo apt update
    sudo apt-get install -y docker-engine
    sudo usermod -aG docker $(whoami)
    exec sudo su ${USER}
    sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)"
    sudo chmod +x /usr/local/bin/docker-compose


Running Mendel,MD using Docker Compose
======================================

    git clone https://github.com/raonyguimaraes/mendelmd/
    cd mendelmd/
    wget https://data.omim.org/downloads/addyourkeyhere/morbidmap.txt -O data/omim/morbidmap.txt
    docker-compose up

Also see how to install it locally without docker-compose here: 

http://mendelmd.readthedocs.io/en/latest/installation.html#manual-installation

# Installation with pip (to-do)
pip3 install rockbio
rockbio runserver

# Installation with conda (to-do)
conda install -c conda-forge rockbio
rockbio runserver

# Local development

git clone https://github.com/rockbio/rockbio
cd rockbio
python3 -m venv venv
source venv/bin/activate
./manage.py migrate
./manage.py runserver
#then on another window for running the background tasks
./manage.py runserver

# Docker Installation
git clone https://github.com/rockbio/rockbio
docker-compose up

# Using Dockerhub
docker run rockbio/rockbio