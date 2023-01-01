from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
        found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        if found_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {vote.post_id} does not exist")
                
        vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                     models.Vote.user_id == current_user.id)
        found_vote = vote_query.first()


        if (vote.dir == 1):
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"User with id {current_user.id} has already voted on Post with id {vote.post_id}")
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Vote successfully registered"}
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with id {current_user.id} has not voted on Post with id {vote.post_id}")
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote successfully removed"}