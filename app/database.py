from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemy_Database_URL='postgresql://postgres:postgres@localhost/fastapi'

engine=create_engine(SQLAlchemy_Database_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()


#           """ FOR DATABASE CONNECTION , WhEN WE DIRECTLY CONNECT OUR DB"""    

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

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


