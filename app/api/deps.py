from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.execptions import CustomException
from app.models.user import User
from app.schemas.token import TokenData
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise CustomException(code=10006, message="username not exist")
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise CustomException(code=40101, message="Token has expired")  # 处理过期的token
    except (jwt.JWTError, ValidationError):
        raise CustomException(code=40103, message="Token validation error")

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise CustomException(code=10006, message="username not exist")
    return user
