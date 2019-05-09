FROM ubuntu:bionic
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN	apt-get install -y apt-utils
RUN	apt-get install -y libterm-readline-gnu-perl
RUN	apt-get upgrade -y
RUN	apt-get install -y \
	bcftools build-essential ca-certificates cpanminus curl gcc git htop libbz2-dev libcgi-session-perl \
	libcurl4-openssl-dev libffi-dev liblocal-lib-perl liblzma-dev libpq-dev libssl-dev libxml2-dev make \
	pkg-config python-dev python-lxml python python-dev python-pip python3 python3-dev python3-pip python3-setuptools python3-venv rabbitmq-server dh-python \
	python3-wheel software-properties-common sudo tabix unzip vcftools vim virtualenvwrapper wget zip zlib1g \
	zlib1g-dev zlibc \
    && apt-get autoremove -y \
	&& apt-get clean
RUN pip3 install -U pip
RUN pip3 install setuptools wheel statistics
RUN pip install statistics
RUN apt-get install -y locales 
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
RUN service rabbitmq-server start
#ADD . /code/
#RUN pip3 install pynnotator
RUN git clone https://github.com/raonyguimaraes/pynnotator.git
RUN cd /code/pynnotator && python3 setup.py develop
#RUN pynnotator install
