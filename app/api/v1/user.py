from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password
from app.services import user as user_service
from app.core.execptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError
from app.services.user import authenticate_user

router = APIRouter()


@router.get('/')
def get_home():
    return {"message": "hello world"}


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service.create_user(db, user)
        return {"message": "user registered successfully"}
    except UserEmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        authenticate_user(db, user.username, user.password)
        return {"message": "Login successful"}
    except LookupError as e:
        raise HTTPException(status_code=400, detail=str(e))
