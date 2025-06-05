https://rutube.ru/plst/299088/

https://hub.docker.com/_/python

```shell
docker build -t ilya.avdeev/words-db ./db/docker
```

```shell
docker run -p 5432:5432 -v $(pwd)/db_content:/var/lib/postgresql/data \
	-v $(pwd)/db/init:/docker-entrypoint-initdb.d \
	-e POSTGRES_PASSWORD=password \
	ilya.avdeev/words-db
```

```shell
$ docker build --no-cache --build-arg OUTPUTDIR_NAME_ARG="/output" --build-arg WORKDIR_NAME_ARG="/usr/src/app" -t voc-translator .
```

```shell
$ docker run -it --rm --name smart-ojegov -v ./result:/output voc-translator
```

