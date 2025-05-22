https://rutube.ru/plst/299088/

https://hub.docker.com/_/python

```shell
$ docker build --no-cache --build-arg OUTPUTDIR_NAME_ARG="/output" --build-arg WORKDIR_NAME_ARG="/usr/src/app" -t voc-translator .
```
    

```shell
$ docker run -it --rm --name smart-ojegov -v ./result:/output voc-translator
```
