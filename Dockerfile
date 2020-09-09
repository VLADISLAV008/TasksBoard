# Creating a docker image and container to run in production:
# 1. docker build --tag boards:1.0 .
# 2. docker run --name test -p 80:80 boards:1.0

FROM python:3
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN python -m pip install uwsgi
RUN pip install uwsgi

COPY . /app/
CMD ["uwsgi", "--ini", "tasks_board/uwsgi.ini"]

FROM nginx:1.15

WORKDIR /app
COPY . /app/

COPY ./tasks_board/nginx.conf /etc/nginx/nginx.conf

