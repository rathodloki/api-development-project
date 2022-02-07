from pydantic import BaseModel
from typing import Optional

class UsersBase(BaseModel):
    name: str
    occupation: Optional[str] = ""
    age: int

class CreateUser(UsersBase):
    pass

class UpdateUser(UsersBase):
    pass

class ResponseUser(UsersBase):
    id: int
    class Config:
        orm_mode = True