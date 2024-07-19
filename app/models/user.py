from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, event
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship

from app.db.base_class import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, comment="用户名称")
    email = Column(String(100), unique=True, index=True, comment="用户邮箱")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, comment="用户是否启用")
    categories = relationship("Category", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)
