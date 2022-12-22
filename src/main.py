#!/usr/bin/env python3

import os
from fastapi import FastAPI
from starlette.requests import Request
from db.postgres import PgConn
from models.items import ItemModel, CreateItemModel, ResponseModel

app = FastAPI()


@app.get("/")
def read_root(request: Request):
    return {"Hello": os.getenv("NAME"), "Browse items": f"{str(request.url)}items"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT item, description from items where id = {item_id};")
        try:
            item, description = cur.fetchone()
            item_schema = ItemModel(id=item_id, item=item, description=description)
            res = item_schema
        except TypeError:
            res = "NOT FOUND!"
    return res


@app.get("/items")
def read_items():
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, item, description from items;")
        try:
            res = [ItemModel(id=_id, item=item, description=description) for _id, item, description in cur.fetchall()]
        except TypeError:
            res = "NOT FOUND!"
    return res


@app.post("/items")
async def create_item(item_model: CreateItemModel):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO items values(default, '{item_model.item}', '{item_model.description}');")
        conn.commit()
    return item_model


@app.patch("/items/{item_id}")
async def update_item(item_id: int, item_model: CreateItemModel):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE items set item = '{item_model.item}', description = '{item_model.description}' "
                    f"WHERE id = {item_id};")
        conn.commit()
    return item_model


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(f"DELETE from items WHERE id = {item_id};")
        conn.commit()
    return ResponseModel(item_id, "DELETED")

