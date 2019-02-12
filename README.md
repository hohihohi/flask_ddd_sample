# flaskd3

flask * ddd micro service application 

## Install

#### Prerequisites

* docker
* docker-compose

```shell
docker-compose build
docker-compose up -d
```

## Run

* run container for development

```
# confirm your uid and gid
$ id
$ cat .env
UID=${YOUR_UID}
GID=${YOUR_GID}
docker network create flaskd3
docker-compose build --no-cache
docker-compose up -d
```

* set up database

```
docker-compose exec -T mysql mysql -uroot -pflaskd3 flaskd3 < sql/create_database.sql
docker-compose exec -T mysql mysql -uroot -pflaskd3 flaskd3 < sql/create_table.sql
```


### Coding style

* directory tree (this project inspired clean-architecture)

```
TBD
```

* Use some make-commands. please see Makefile.
* [reference](https://nrslib.com/clean-flow-of-control/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
