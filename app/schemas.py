from pydantic import BaseModel

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