# Creating a docker image and container to run in production:
# 1. docker build --tag boards:1.0 .
# 2. docker run --name test -p 80:80 boards:1.0

FROM tiangolo/uwsgi-nginx:python3.8

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN python -m pip install uwsgi
COPY . /app/

ENV UWSGI_INI /app/tasks_board/uwsgi.ini
COPY ./tasks_board/nginx.conf /etc/nginx/nginx.conf