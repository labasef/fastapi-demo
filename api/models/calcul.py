from pydantic import BaseModel, Field
from typing import List


class AddModel(BaseModel):
    numbers: List[int] = Field(...)

    class Config:
        schema_extra = {
                "numbers": [1, 2]
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
