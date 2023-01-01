from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Users']
)

# my_posts = [{"title": "1", "content": "1", "id": 1}, {"title": "2", "content": "2", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @router.get("/sqlalchemy")
# def root(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"message": posts}

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user), # current_user is not of type int but yet works
                limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
                # search is Optional as no default search filter should be applied
    
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    # fetchone over fetchall when id exists in only one row
    # why go through all when you have already found the one
    # and know thats it

    # limit gives those many rows and offset then skips over some rows
    # so limit = 5 gives 5 rows and offset = 2 skips over first 2 rows
    # and gives the remaining 3 rows

    # posts = db.query(models.Post).limit(limit).offset(skip).all()
    
    # uses left outer join when isouter=True
    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    print(query)
    posts = query.all()

    return posts

## casting later does not work
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
 # mentioned that db can be done inside, tried (not much) didnt work out
    # does not work. not preferred because of sql injection attack
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")

    # psycopg2 checks for sql injection attacks
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # need to commit so the changes are reflected back in the database
    # conn.commit()

    # can become very inefficient if no. of cols is large
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    
    # **post.dict() returns the form as - title=post.title, content=post.content,...

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




# @router.get("/posts/latest")
# def get_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # if comma is absent then for id = 90 -> internal server error
    # cursor.execute(""" SELECT * FROM posts where id = %s""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")

    # user can view his own specific post only
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    return post

# @router.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"detail": f"Post with {id} was not found"}
#     return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # comma here as well
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}")    
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    if query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform the requested action")

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return query.first()