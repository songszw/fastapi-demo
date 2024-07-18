from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: EmailStr


class UserLogin(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
