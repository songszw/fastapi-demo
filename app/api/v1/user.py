from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.api.deps import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.schemas.response import ResponseModel
from app.schemas.user import UserCreate, UserLogin, UpdatePasswordRequest, LoginRequest
from app.services import user as user_service
from app.core.execptions import UserEmailAlreadyExistsError, UsernameAlreadyExistsError, LoginError, CustomException, \
    PasswordError, UserNotFoundError
from app.services.user import login_for_access_token, update_user_password

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service.create_user(db, user)
        return ResponseModel(code=200, message="user registered successfully")
    except UserEmailAlreadyExistsError as e:
        return ResponseModel(code=10002, message=str(e))
        # raise HTTPException(status_code=400, detail=str(e))
    except UsernameAlreadyExistsError as e:
        return ResponseModel(code=10001, message=str(e))
        # raise HTTPException(status_code=400, detail=str(e))


@router.post('/login')
def login(user: LoginRequest, db: Session = Depends(get_db)):
    try:
        token_data = login_for_access_token(db, user.username, user.password)
        return ResponseModel(code=200, data=token_data, message='Login successful')
    except HTTPException as e:
        return ResponseModel(code=10005, message=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}")


@router.put('/password')
def update_password(
        update_password_request: UpdatePasswordRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        # 尝试更新用户密码
        update_user_password(
            db=db,
            user=current_user,
            current_password=update_password_request.current_password,
            new_password=update_password_request.new_password
        )
        return ResponseModel(code=200, message="Password updated successfully")
    except PasswordError as e:
        return ResponseModel(code=10005, message=str(e))
    except CustomException as e:
        return ResponseModel(code=e.code, message=e.message)
    except Exception as e:
        # 捕获其他异常并返回500错误
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('', response_model=schemas.ResponseDataModel[schemas.UserInfo])
def user_info(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = user_service.get_user_info(db, user_id=current_user.id)
        return schemas.ResponseDataModel(code=200, data=result, message="success")
    except UserNotFoundError as e:
        return schemas.ResponseDataModel(code=10006, message=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}")
