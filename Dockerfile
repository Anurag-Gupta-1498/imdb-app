FROM python:3.8.10-slim

ADD req.txt /app/requirements.txt

RUN apt-get update -y 

RUN apt-get install python3-dev build-essential -y

RUN set -ex \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --upgrade pip setuptools wheel \
    && /env/bin/pip3 install --no-cache-dir -r /app/requirements.txt

ADD . /app

WORKDIR /app

RUN mkdir -p /var/log/gunicorn/

ENV VIRTUAL_ENV /env

ENV PATH /env/bin:$PATH

RUN python manage.py collectstatic --no-input

RUN python manage.py migrate

CMD gunicorn --workers=2 imdbapp.wsgi:application --bind 0.0.0.0:$PORT
