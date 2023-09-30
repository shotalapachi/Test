from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "nika2",
                "password": "nika2"
            }
        }
