from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UpdatePasswordRequest, LoginRequest
from app.services import user as user_service
from app.core.execptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError, LoginError
from app.services.user import login_for_access_token, update_user_password

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
def login(user: LoginRequest, db: Session = Depends(get_db)):
    return login_for_access_token(db, user.username, user.password)


@router.put('/password')
def update_password(
        update_password_request: UpdatePasswordRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        update_user_password(
            db=db,
            user=current_user,
            current_password=update_password_request.current_password,
            new_password=update_password_request.new_password
        )
        return {"message": "Password update successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
