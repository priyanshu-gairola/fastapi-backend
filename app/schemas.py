from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
  title:str
  content:str
  published:bool=True
  #rating:Optional[int]=None
#connecting databse

class Post(PostBase):
  pass

class CreatePost(PostBase):
  pass

class PostResponse(PostBase):
  id:int
  created_at:datetime

  class Config:
    orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
      orm_mode=True
    