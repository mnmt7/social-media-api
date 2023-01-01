# __init__py ensures that the folder it is in, is a package
# postgres comes with default database named postgres
# as it requires a database to make the connection

# pydantic model provides the structure for request and response
# sqlalchemy model provides the structure of table i.e. the columns 

# observation -> until we dont apply one revision, we cannot create other

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# not required as now using alembic
# models.Base.metadata.create_all(bind=engine)

# pip install -r requirements.txt

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com"
]

# middleware is a function that is run before request is sent to the routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}