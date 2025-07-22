from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemy_Database_URL='postgresql://postgres:postgres@localhost/fastapi'

engine=create_engine(SQLAlchemy_Database_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False)

Base=declarative_base()

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()

