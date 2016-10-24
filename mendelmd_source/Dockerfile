FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.stable.txt /code/
RUN apt-get update
RUN apt-get -y install libcurl4-gnutls-dev gcc git python3-dev zlib1g-dev virtualenvwrapper
RUN pip install -r requirements.stable.txt
ADD . /code/