FROM python:3.6

EXPOSE 8000

ADD . /www
WORKDIR /www

RUN pip3 install -r app/requirements.txt && pip3 install uwsgi

CMD ["uwsgi", "--ini", "uwsgi.ini"]

