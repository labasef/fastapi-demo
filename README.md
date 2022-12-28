# Fast API Demo

This project is used to demonstrate Fast API and can also be used as a template for projects requiring an API.

## Prerequisites :computer:

This project uses `docker` and `docker-compose` (version 3.9).

## External documentation :clipboard:

- [docker-compose](https://docs.docker.com/compose/ "docker-compose")
- [dockerfile](https://docs.docker.com/engine/reference/builder/ "dockerfile")
- [PostgreSQL](https://www.postgresql.org/docs/15/index.html "postgresql")
- [FastAPI](https://fastapi.tiangolo.com/ "fastapi")

## Overview :eyes:

This project is made of two docker container.
The first one hosts the postgresql database.
The second one serves the API.

An additional scriptlet `api.py` acts as a wrapper for the HTTP methods.

### Environment

Environment variables are set in the `.env` file. The environment variables are used across the project for example for defining database connection parameters once and for all. To make them accessible from inside a docker container, you should pass them in the service definition in the `docker-compose.yml` file. The variables passed to the docker container can be accessed in python using `os.getenv("VARIABLE")`.

When you add and/or change an environment variable in the `.env` file, you will need to recreate and restart the container using `docker-compose up`.

### Tools

The file `.tools` provides aliases and functions useful for this project. To use it:
```
source .tools
```
The available tools are the following:

- `runapi` performs the docker-compose up
- `fastapi [-h] [--url URL] [--https [HTTPS]] {get,post,patch,put,delete} [path] [body]` performs a request on the API
- `postgres` opens a shell connection to the postgres database
- `create_items_table` creates the items table

### Data model :page_facing_up:

The data model was kept as simple as possible for this demo. It is made of a single table *items* with three columns: id, item, description; where id is a primary key.

```
   Column    |          Type          | Collation | Nullable |              Default              
-------------+------------------------+-----------+----------+-----------------------------------
 id          | integer                |           | not null | nextval('items_id_seq'::regclass)
 item        | character varying      |           | not null | 
 description | character varying(255) |           |          | 
Indexes:
    "items_pkey" PRIMARY KEY, btree (id)
```

### API :robot:

The API layer allows interactions with the database through the provided endpoints.
CRUD operations on items are available:

- Create: http POST
- Read: http GET
- Update: http PATCH
- Delete: http DELETE

## Build :wrench:

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

Once your project is up and running, if not in detached mode, you will see the following log line:
```
fastapi_app | INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

## Usage :fire:

The API is served on your local host on port 8 (port mapping is defined in the docker-compose.yml):
[Try it here](https://localhost:8/ "fastapi_demo")

Note: if the API runs on an AWS VM, you will need to forward port 8 of your local machine:
```
qcc tunnel 8 [--machine <ec2_fastapi>]
```

### Documentation :pencil:

:star2: Fast API generates the endpoints' documentation automatically:
[See the documentation](https://localhost:8/docs "fastapi_demo - docs")

### Endpoints :round_pushpin:

- Welcome page: GET https://localhost:8/
- Add numbers together: POST https://localhost:8/addition body json {"numbers": [int]}
- List all items: GET https://localhost:8/items
- See an item: GET https://localhost:8/items/{item_id}
- Create an item: POST https://localhost:8/items body: json {"item": "item denomination", "description": "item description"} 
- Update an item: PATCH https://localhost:8/items/{item_id} body: json {"item": "updated item denomination", "description": "updated item description"}
- Delete an item: DELETE https://localhost:8/items/{item_id}

## API Clients

For GET requests, you can use your web browser and simply enter the url of the endpoint you want to request.

### Postman :rocket:

[Postman](https://www.postman.com/) is a complete API platform for building, testing and using APIs. You can save requests and build entire test scenarii.

### Python requests package

[Documentation](https://requests.readthedocs.io/en/latest/) This is a widely used Python package when dealing with API. If you are building a client application to a FastAPI application, you will definitely need to use it.

### CLI

If you work on a VM with no GUI, using the command line interface may be your only option. There are tools you can use or you can build your own.

- [CURL](https://curl.se/) - This is the most widely used command line tool for interacting with APIs. Even though it comes in really handy, it can be a hassle if you are not familiar whith shell.
- Wrapper - Using python' requests, you can build a wrapper for the API endpoints. In this demo project, a python wrapper is provided. see the documentation in the next section:

#### api.py wrapper

Basic usage:

```
usage: api.py [-h] [--url URL] [--https [HTTPS]] {get,post,patch,put,delete} ...

A simple wrapper to perform http on an API

positional arguments:
  {get,post,patch,put,delete}
                        types of http methods

options:
  -h, --help            show this help message and exit
  --url URL             The target api url; do not put the http://
  --https [HTTPS]       Whether to use https method; default: False
```

Usage for **GET**:

```
usage: api.py get [-h] [path]

positional arguments:
  path        The path to get; do not put the full url. ex: /items

options:
  -h, --help  show this help message and exit
```

Usage for **POST**:

```
usage: api.py post [-h] path body

positional arguments:
  path        The path to post; do not put the full url. ex: /items
  body        The body to post; should be a json string

options:
  -h, --help  show this help message and exit
```

Usage for **PATCH**:

```
usage: api.py patch [-h] path body

positional arguments:
  path        The path to patch; do not put the full url. ex: /items/2
  body        The body to patch; should be a json string

options:
  -h, --help  show this help message and exit
```

Usage for **PUT**:

```
usage: api.py put [-h] path body

positional arguments:
  path        The path to put; do not put the full url. ex: /items/2
  body        The body to put; should be a json string

options:
  -h, --help  show this help message and exit
```

Usage for **DELETE**:

```
usage: api.py delete [-h] path

positional arguments:
  path        The path to delete; do not put the full url. ex: /items/2

options:
  -h, --help  show this help message and exit
```

This simple wrapper can be used for any API. For the purpose of this demo project, an alias was created in the .tools file: `alias fastapi="python3 api.py --url localhost:${FASTAPI_PORT}"` As a result, after sourcing the .tools file `source .tools` you can use it simply:

example of **creating** an item (id is autoincrement, in this case id=7), **retreiving** it, **updating** its description and **deleting** it: 
```
fastapi post /items '{"item":"bottle","description":"a bottle is a closed container designed to hold a liquid"}'

>>> {"item":"bottle","description":"a bottle is a closed container designed to hold a liquid"}
```
```
fastapi get /items/7

>>> {"id":7,"item":"bottle","description":"a bottle is a closed container designed to hold a liquid"}
```
```
fastapi patch /items/7 '{"item":"bottle","description":"a bottle is a closed container designed to hold a liquid, ex: a water bottle"}'
>>> {"item":"bottle","description":"a bottle is a closed container designed to hold a liquid, ex: a water bottle"}
```
```
fastapi delete /items/7
>>> {"data":[7],"code":200,"message":"DELETED"}
```

