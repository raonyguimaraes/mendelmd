# Mendel,MD a user-friendly online program for clinical exome and genome analysis

An online tool for annotating, filtering and analysing both genomes and exomes to help with the diagnosis of patients with Mendelian Disorders.

https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-16-S8-A2

Try our new test server on https://mendelmd.org

OMIM Data
=========

You need to register at OMIM: http://omim.org/downloads and submit a download request to get a file named "morbidmap.txt".

After obtaining this file you will need to put it on the folder: "mendelmd_source/data/omim/".


Running Mendel,MD using Docker Compose
======================================
    
    git clone https://github.com/raonyguimaraes/mendelmd/
    cd mendelmd/mendelmd_source/
    wget https://data.omim.org/downloads/addyourkeyhere/morbidmap.txt -O data/omim/morbidmap.txt
    docker-compose up


Requirements
============

* At least 60GB of disk space
* Python 3.4+
* Perl 5.8+
* Java 1.8
* Ubuntu LTS 16.04

OR

* Docker
* Docker Compose

Installation of docker and docker-compose on Ubuntu 16.04 LTS
=============================================================

    sudo apt-get update
    sudo apt-get install software-properties-common apt-transport-https
    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
    sudo apt update
    sudo apt-get install -y docker-engine
    sudo usermod -aG docker $(whoami)
    #You will need to log out of the Droplet and back in as the same user to enable this change.

    sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)"
    sudo chmod +x /usr/local/bin/docker-compose
