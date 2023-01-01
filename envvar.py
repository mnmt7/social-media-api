# import os

# path = os.getenv("PATH")
# print(path)

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"

data = {
    "message": "this is a token",
    "value": 123,
    "another message": "this is a jwt token",
    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
}


encoded_data = jwt.encode(data, SECRET_KEY, ALGORITHM)

print(encoded_data)
