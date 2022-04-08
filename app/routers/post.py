from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model = List[schemas.Post]) ## Change return from results back to post to use.
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), \
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 10, skip: int = 0, 
    search: Optional[str] = ''):
    # This will limit the amount of posts the user would like to retrieve
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, \
        func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, 
        isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(
                limit).offset(skip).all()

    
    # This will retrieve all the posts in the database.
    # posts = db.query(models.Post).all()

    # This will restrict the posts returned to only the user logged in.
    # posts = db.query(models.Post).fileter(models.Post.owner_id == current_user.id).all()
    return results

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # Create a variable to catch and return the RETURNING command.
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Order matters.  This must be above the @app.get("/posts/{id}").
# Because {id} is technically a variable, it could evaluate to @app.get("/posts/latest")
# and this latest function would never be called.
# @app.get("/posts/latest", response_model = schemas.Post)
# def get_latest_post():
#     cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
#     latest_post = cursor.fetchone()
#     return latest_post

# {id} == "Path Parameter"

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = {0} """.format(str(id)))
    # post = cursor.fetchone() 
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, \
        func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, 
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id}, was not found.')

    # This logic will only allow the user logged in to pull a single post that belongs to them.
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, \
    #         detail = f"Not authorized to perform requested action.")
    
        
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleting post
    # find the index in the list that has required id.
    # my_posts.pop(index)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, \
            detail = f"Post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, \
            detail = f"Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def update_post(id: int, posts: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    # (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone() 
    # conn.commit() 
     
    post_query = db.query(models.Post).filter(models.Post.id == id) 

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, \
            detail= f"Post with id: {id} not found.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, \
            detail = f"Not authorized to perform requested action.")

    post_query.update(posts.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()