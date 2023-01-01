import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: int= 5432
    database_name: str= "api"
    database_username: str= "postgres"
    database_password: str= "somePassword"
    secret_key: str= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str= "HS256"
    access_token_expire_minutes: int=30

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"

settings = Settings()