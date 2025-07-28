
from fastapi import HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from .. import schemas,models
from ..database import get_db
from typing import List
from .. import utils

router=APIRouter(prefix="/users")


#create users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

  hashed_pw=utils.hash(user.password)
  user.password=hashed_pw
  new_user=models.User(**user.dict())  #unpacking dict
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

#get users by id

@router.get("/{id}",response_model=schemas.UserOut)
def get_user_by_ID(id:int,db:Session=Depends(get_db)):
  user=db.query(models.User).filter(models.User.id==id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} not found")
  return user