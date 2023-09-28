from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
 
from models.postModel import Posts
from schemas.postSchemas import PostSchemas
from db.database import SessionLocal, engine
from  models import postModel

from typing import List

postModel.Base.metadata.create_all(bind=engine)

posts = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@posts.get('/post', response_model=List[PostSchemas])
def get_all_post(db: Session = Depends(get_db)):
    posts = db.query(postModel.Posts).all()  # Utiliza el modelo Post y no postModel.Post
    return posts

@posts.get('/post/{post_id}', response_model=PostSchemas)  # Usar PostSchemas en lugar de Posts
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    return post


@posts.post('/createpost')
def make_post(post: PostSchemas, db: Session = Depends(get_db)):
     db_post = postModel.Posts(title = post.title, description=post.description)
     db.add(db_post)
     db.commit()
     return {"message":"Post Added"}


@posts.delete('/post/{post_id}', response_model=dict)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": f"Post with id {post_id} has been deleted"}

@posts.put('/post/{post_id}', response_model=PostSchemas)
def update_post(post_id: int, post_data: PostSchemas, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")

    # Actualiza los campos del post con los datos proporcionados
    post.title = post_data.title
    post.description = post_data.description

    db.commit()

    return post