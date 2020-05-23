# ReserveRoom
KHU Classroom Reservation Service

## Quickstart
Docker, Docker-Compose
```
$ git clone https://github.com/freckie/reserveroom
$ cd reserveroom

$ cd nginx
$ docker build --tag reserveroom_nginx .
$ cd ..

$ cd reserveroom_api
$ docker build --tag reserveroom_api .
$ cd ..

$ docker-compose up -d
```