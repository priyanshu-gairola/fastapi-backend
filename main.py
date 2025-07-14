from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class Post(BaseModel):
  title:str
  content:str
  published:bool=True
  rating:Optional[int]=None

@app.get('/')
def root():
  return {"message":"Hey ! made by Priyanshu"}

@app.get('/hello/{name}')
def hello(name):
  return f"Welcome {name}"

@app.post("/createpost")
def create_post(post:Post):
  print(post.title)
  print(post.content)
  print(post.rating)
  return post



