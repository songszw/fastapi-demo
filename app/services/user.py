from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.execptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError, LoginError
from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise LoginError()
    return user
