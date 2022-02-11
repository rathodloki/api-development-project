from pydantic import BaseModel, EmailStr
from typing import Optional

class UsersBase(BaseModel):
    name: str
    occupation: Optional[str] = ""
    age: int

class CreateUser(UsersBase):
    email: EmailStr
    password: str
    pass

class UpdateUser(UsersBase):
    pass

class ResponseUser(UsersBase):
    email: EmailStr
    class Config:
        orm_mode = True