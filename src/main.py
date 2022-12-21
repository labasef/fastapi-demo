#!/usr/bin/env python3

import os
from fastapi import FastAPI
from db.postgres import PgConn
from models.items import ItemSchema, UpdateItemModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": os.getenv("NAME")}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT item, description from items where id = {item_id};")
        try:
            item, description = cur.fetchone()
            item_schema = ItemSchema(id=item_id, item=item, description=description)
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
            res = [ItemSchema(id=_id, item=item, description=description) for _id, item, description in cur.fetchall()]
        except TypeError:
            res = "NOT FOUND!"
    return res


@app.post("/items")
async def create_item(item_model: UpdateItemModel):
    with PgConn(os.getenv('POSTGRES_DB')) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(f"INSERT INTO items values(default, '{item_model.item}', '{item_model.description}');")
        conn.commit()
    return item_model

