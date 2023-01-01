# sqlalchemy does not know how to communicate with database
# so we need to provide the driver so sqlalchemy can communicate
# with the database

# since we need to communicate with postgres, we can use the
# psycopg2 package

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# returns session to the database
# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#using sqlalchemy so of no use
# if database has not yet initialized or ...
# while True:
#     # connection to a database can fail due to no. of issues, so inside the try block
#     try:
#         # havent updated it with environment variables
#         conn = psycopg2.connect(host='localhost', database='api', user='postgres',
#         password='somePassword', cursor_factory=RealDictCursor) 
#         # using cursor factory so as to get the col names along with rows
#         # hard coded the credentials and other things
#         # it will be git
#         # this is development environment and values for production environment might be different
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)