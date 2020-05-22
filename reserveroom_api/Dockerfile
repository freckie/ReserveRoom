FROM python:3.6

ADD . /www
WORKDIR /www

RUN pip3 install -r ./requirements.txt && pip3 install uwsgi

CMD uwsgi uwsgi.ini

