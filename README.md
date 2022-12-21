# Fast API Demo

This project is used to demonstrate Fast API and can also be used as a template for projects requiring an API.

## Prerequisites 

This project uses `docker` and `docker-compose` (version 3.9).

## External documentation

- [docker-compose](https://docs.docker.com/compose/ "docker-compose")
- [dockerfile](https://docs.docker.com/engine/reference/builder/ "dockerfile")
- [PostgreSQL](https://www.postgresql.org/docs/15/index.html "postgresql")
- [FastAPI](https://fastapi.tiangolo.com/ "fastapi")

## Overview

This project is made of two docker container.
The first one hosts the postgresql database.
The second one serves the API.

An additional scriptlet `get-api.py` acts as a wrapper for the HTTP GET method.

## Build

In order to to build the project, from the folder where the `docker-compose.yml` file is, use the following command:

```
docker-compose up -d
```
Note: the "-d" argument means detached mode. If you need to see the logs, do not use it; the docker process will be attached to the terminal.

It is possible you get the following error when rebuilding the project:
```
error checking context: 'can't stat '[...]/fastapi_demo/data/postgres-db-volume''.
ERROR: Service 'fastapi' failed to build : Build failed
```
This happens because the postgres-db-volume is not owned by your user. To make it yours, run:
```
sudo chown -R $USER data/postgres-db-volume
```

Once your project is up and running, if not in detached mode you will see the following log line:
```
fastapi_app | INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

## Usage

The API is serve on your local host on port 8 (port mapping is defined in the docker-compose.yml):
[Try it here](https://localhost:8/ "fastapi_demo")

Note: if the API rune on an AWS VM, you will need to forward port 8 of your local machine:
```
qcc tunnel 8 [--machine <ec2_fastapi>]
```


