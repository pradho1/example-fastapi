from charset_normalizer import models
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import database, models

from starlette.status import HTTP_401_UNAUTHORIZED
from . import schemas
from . config import settings   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#Secret_Key
#Algorithm
#Expiration_time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expires_in = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires_in})
    endcoded_jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return endcoded_jwt_token

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        email:EmailStr = payload.get("email")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, email=email)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user




