from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
        limit: int=10, skip:int = 0, search:str = ""):
    #posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if posts == None:
        return {"data" : "No data found"}
    else:
        return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()

    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exists.")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform the requested operation.")
    return posts

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, update_data_post:schemas.PostCreate, db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exists.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to perform requested operation")
    post_query.update(update_data_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} does not exists." )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to perform requested operation")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


