from fastapi import FastAPI,HTTPException, Response,status,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import get_db,engine
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from . import utils
from . routers import post,user,auth

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


# while True:
#   try:
#     conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',
#                           cursor_factory=RealDictCursor)
    
#     cursor=conn.cursor()
#     print("Database connected successfully")
#     break  #once connected break the loop


#   except Exception as error:
#     print("Unable to connect database")
#     print("Error:",error)  
#     time.sleep(3)  #wait for 3 second and retry to connect db



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

# def find_post(id):
#   for post in my_posts:
#     if post["id"]==id:
#       return post
    
# def find_index(id):
#   for i,p in enumerate(my_posts):
#     if p["id"]==id:
#       return i

@app.get('/')
def root():
  return {"message":"Hey ! made by Priyanshu"}

#including routers from other files also
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
