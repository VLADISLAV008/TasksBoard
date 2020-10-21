# Creating a docker image and container to run in production:
# 1. docker build --tag boards:1.0 .
# 2. docker run --name test -p 80:80 boards:1.0

FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN python -m pip install uwsgi
COPY . /app/

RUN apt-get update && apt-get -y install gcc postgresql \
  && apt-get clean

ENV UWSGI_INI /app/tasks_board/uwsgi.ini
ENV STATIC_PATH /app/static