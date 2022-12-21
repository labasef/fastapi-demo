from typing import Optional

from pydantic import BaseModel, Field


class ItemSchema(BaseModel):
    id: int = Field(...)
    item: str = Field(...)
    description: str = Field(...)

    class Config:
        schema_extra = {
                "id": 1,
                "item": "table",
                "description": "a table is a furniture with a flat top on which to put things"
        }


class UpdateItemModel(BaseModel):
    item: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
                "item": "table",
                "description": "a table is a furniture with a flat top on which to put things"
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
