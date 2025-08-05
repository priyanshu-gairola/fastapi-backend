from fastapi import HTTPException,Depends,status,APIRouter,Response
from sqlalchemy.orm import Session
from .. import schemas,models
from ..database import get_db
from ..Oauth import get_current_user
from typing import List

router=APIRouter(
  prefix="/posts",
  tags=["Post"]
  )

@router.get("/",response_model=List[schemas.PostResponse])
def get_all_posts(db:Session=Depends(get_db)):
  # cursor.execute(""" SELECT * FROM posts """)
  # posts=cursor.fetchall()

  all_posts=db.query(models.Post).all()
  return all_posts

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post_by_id(id:int,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
  # post=cursor.fetchone()

  post=db.query(models.Post).filter(models.Post.id==id).first()
  if post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id:{id} not found."
    )

  return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.Post,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
  # cursor.execute(""" INSERT INTO posts (title,content,published)
  #                 VALUES(%s,%s,%s) RETURNING *""",
  #                 (post.title,post.content,post.published))
  # new_posts=cursor.fetchone()
  # conn.commit()  #to save in db

  new_post=models.Post(**post.dict())  #unpacking dict
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return new_post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
  # cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""",(str(id)))
  # deleted_post=cursor.fetchone()
  # conn.commit()

  deleted_post=db.query(models.Post).filter(models.Post.id==id).first()
  
  if deleted_post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} not found")
  
  db.delete(deleted_post)
  db.commit()
  

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}')
def post_update(id:int,updated_post:schemas.Post,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
  # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
  #                (post.title,post.content,post.published,str(id)))
  # updated_post=cursor.fetchone()
  # conn.commit()
  post_query=db.query(models.Post).filter(models.Post.id==id)

  post=post_query.first()

  if post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id:{id} not found")
  
  post_query.update(updated_post.dict(),synchronize_session=False)
  db.commit()

  return "Post updated successfully"





