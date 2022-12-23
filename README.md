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

An additional scriptlet `get-api.py` acts as a wrapper for the HTTP GET method.

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


### Tools

The file `.tools` provides aliases and functions useful for this project. To use it:
```
source .tools
```
The available tools are the following:

- `runapi` performs the docker-compose up
- `fastapi [-h] [--url URL] [--https [HTTPS]] {get,post,patch,put,delete} [path] [body]` performs a request on the API
- `postgres` opens a shell connection to the postgres database
