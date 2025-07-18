from fastapi import FastAPI,HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()

class Post(BaseModel):
  title:str
  content:str
  published:bool=True
  rating:Optional[int]=None

my_posts=[
   {"title":"Kandara",
    "content":"Beautiful village in uttarakhand",
    "published":True,
    "rating":10,
    "id":1
    },
    {
    "title":"Ddun",
    "content":"Beautiful city in uttarakhand",
    "published":False,
    "rating":8,
    "id":2
    }
    ]

def find_post(id):
  for post in my_posts:
    if post["id"]==id:
      return post
    
def find_index(id):
  for i,p in enumerate(my_posts):
    if p["id"]==id:
      return i

@app.get('/')
def root():
  return {"message":"Hey ! made by Priyanshu"}

@app.get('/posts')
def get_all_posts():
  return my_posts

@app.get("/posts/{id}")
def get_post_by_id(id:int):
  post=find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id:{id} not found."
    )
  return {"post_details":post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
  post_dict=post.dict()
  post_dict["id"]=randrange(0,100000)
  my_posts.append(post_dict)
  return {"data":post_dict}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
  index=find_index(id)
  if index==None:
    return {"message":f"Post with id:{id} not found"}
  my_posts.pop(index)
  return Response(status_code=204)

@app.put('/posts/{id}')
def post_update(id:int,post:Post):
  index=find_index(id)
  if index==None:
    return {"message":f"Post with id:{id} not found"}

  post_dict=post.dict()
  post_dict["id"]=id
  my_posts[index]=post_dict

  return {"message":"Post updated successfully" }
  


