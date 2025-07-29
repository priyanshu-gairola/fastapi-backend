from fastapi import HTTPException,Depends,status,APIRouter
from sqlalchemy.orm import Session
from .. import schemas,models
from ..database import get_db
from typing import List
from .. import utils
from .. import Oauth

router=APIRouter()

@router.post("/login")
def login(user_cred:schemas.UserLogin,db:Session=Depends(get_db)):
  user=db.query(models.User).filter(models.User.email==user_cred.email).first()
  if user==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Invalid Credentials")
  
  if not utils.verify_password(user_cred.password,user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Invalid Credentials")
  
  access_token=Oauth.create_access_token(data={"id":user.id})
  
  return {"token":access_token , "token_type":"bearer"}

