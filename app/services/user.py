from datetime import timedelta, datetime
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.execptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError, LoginError
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.db_service import save_to_db


def create_user(db: Session, user: UserCreate):
    if get_user_by_email(db, user.email):
        raise UserEmailAlreadyExistsError(f"User with email {user.email} already exists")
    if get_user_by_username(db, user.username):
        raise UsernameAlreadyExistsError(f"Username {user.username} already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    return save_to_db(db, db_user)


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise LoginError()
    return user


def login_for_access_token(db: Session, username: str, password: str):
    try:
        user = authenticate_user(db, username, password)
    except LoginError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def update_user_password(db: Session, user: User, current_password: str, new_password: str):
    if not user.verify_password(current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    user.hashed_password = bcrypt.hash(new_password)
    return save_to_db(db, user)

