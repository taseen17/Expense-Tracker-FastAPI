from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from typing import Annotated
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = 'c3b1f32b100cfa5da58e0825289b20a8a3ff3ab22afe492cd897bec6055d6e5b'
ALGORITHM = 'HS256'

class CreateUsers(BaseModel):
    username: str
    email: str
    password: str


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return None
    if bcrypt_context.verify(password, user.hashed_password):
        return user
    return None

def create_access_token(username: str, user_id: int, expires_delta: timedelta ):
    encode = {"sub": username, "user_id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise JWTError
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from exc
    return {"username": username, "user_id": user_id, "role": role}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/auth")
def authenticate():
    return {"message": "Authentication endpoint"}

@router.post("/auth/register")
def register_user(user: CreateUsers, db: db_dependency):
    hashed_password = bcrypt_context.hash(user.password)
    db_user = Users(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(content={"message": "User registered successfully", "user_id": db_user.id}, status_code=201)


@router.post("/auth/login")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        return JSONResponse(content={"message": "Invalid username or password"}, status_code=401)

    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}