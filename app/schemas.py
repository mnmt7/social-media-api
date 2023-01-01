from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime 
    owner_id: int 
    owner: UserOut 
    # attribute "owner" having the same name as defined in the corresponding model
    # pretty basic if you understand the other attributes also follow the same convention

    # votes: int

    class Config:
        orm_mode = True
    # From the docs - https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    #  but an ORM model (or any other arbitrary object with attributes).
    # This way, instead of only trying to get the id value from a dict, as in:
    # id = data["id"]
    # it will also try to get it from an attribute, as in:
    # id = data.id

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)