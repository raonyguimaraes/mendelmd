FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.stable.txt /code/
RUN apt-get update
RUN apt-get -y install gcc git python3-dev zlib1g-dev virtualenvwrapper
RUN pip install -r requirements.stable.txt
ADD . /code/

