FROM ubuntu:xenial
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.stable.txt /code/
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y \
	libcurl4-gnutls-dev gcc git python3-dev zlib1g-dev virtualenvwrapper make zip python3-pip sudo \
	build-essential bcftools software-properties-common \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    && apt-get autoremove -y \
	&& apt-get clean
RUN pip3 install -U pip setuptools
RUN pip3 install cython==0.24.1 
RUN pip3 install pynnotator
RUN pynnotator install
RUN pip3 install -r requirements.stable.txt
ADD . /code/
RUN python3 manage.py migrate auth
RUN python3 manage.py migrate
RUN python3 manage.py populate
RUN python3 manage.py collectstatic --noinput