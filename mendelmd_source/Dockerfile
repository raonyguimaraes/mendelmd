FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update
RUN	apt-get install -y apt-utils
RUN	apt-get install -y libterm-readline-gnu-perl
#RUN	apt-get upgrade -y
RUN	apt-get install -y \
	bcftools build-essential ca-certificates cpanminus curl gcc git htop libbz2-dev libcgi-session-perl \
	libcurl4-openssl-dev libffi-dev liblocal-lib-perl liblzma-dev libpq-dev libssl-dev libxml2-dev make \
	pkg-config python-dev python-lxml python3 python3-dev python3-pip python3-setuptools python3-venv \
	python3-wheel software-properties-common sudo tabix unzip vcftools virtualenvwrapper wget zip zlib1g \
	zlib1g-dev zlibc \
    && apt-get autoremove -y \
	&& apt-get clean
RUN pip3 install -U pip
RUN pip3 install setuptools wheel
RUN pip3 install pynnotator
RUN pynnotator install
RUN pip3 install -r requirements.txt
ADD . /code/