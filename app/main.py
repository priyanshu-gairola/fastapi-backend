from fastapi import FastAPI,HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app=FastAPI()

class Post(BaseModel):
  title:str
  content:str
  published:bool=True
  #rating:Optional[int]=None
#connecting databse

while True:
  try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',
                          cursor_factory=RealDictCursor)
    
    cursor=conn.cursor()
    print("Database connected successfully")
    break  #once connected break the loop


  except Exception as error:
    print("Unable to connect database")
    print("Error:",error)  
    time.sleep(3)  #wait for 3 second and retry to connect db



# my_posts=[
#    {"title":"Kandara",
#     "content":"Beautiful village in uttarakhand",
#     "published":True,
#     "rating":10,
#     "id":1
#     },
#     {
#     "title":"Ddun",
#     "content":"Beautiful city in uttarakhand",
#     "published":False,
#     "rating":8,
#     "id":2
#     }
#     ]

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
  cursor.execute(""" SELECT * FROM posts """)
  posts=cursor.fetchall()
  return {"message":posts}

@app.get("/posts/{id}")
def get_post_by_id(id:int):
  cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
  post=cursor.fetchone()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id:{id} not found."
    )
  return {"post_details":post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
  cursor.execute(""" INSERT INTO posts (title,content,published)
                  VALUES(%s,%s,%s) RETURNING *""",
                  (post.title,post.content,post.published))
  new_posts=cursor.fetchone()
  conn.commit()  #to save in db

  return {"data":new_posts}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
  cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""",(str(id)))
  deleted_post=cursor.fetchone()
  conn.commit()

  if deleted_post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} not found")

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def post_update(id:int,post:Post):
  cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
                 (post.title,post.content,post.published,str(id)))
  updated_post=cursor.fetchone()
  conn.commit()
  if updated_post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} not found")

  return {"message":"Post updated successfully" }
  


