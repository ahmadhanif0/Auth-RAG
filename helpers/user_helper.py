from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from models.user import User
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()


ph = PasswordHasher()

KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict, expires_delta:Optional[timedelta]=None)-> str:
    to_encode = data.copy()
# HHH
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp" : expire})
    encode_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        email : str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="User information is not found.")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    email = payload.get("sub")
    user = await User.get_or_none(email=email)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user