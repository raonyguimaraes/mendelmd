FROM python:3.6
RUN mkdir -p /code
WORKDIR /code
RUN apt-get update && \
    apt-get install -y locales \
  && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ADD requirements.txt .
RUN ls -l
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
ADD . /code/