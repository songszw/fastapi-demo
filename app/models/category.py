from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, event
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, comment="类目id")
    name = Column(String(50), index=True, comment="类目名称")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment="类目所属用户id")
    user = relationship("User", back_populates="categories")
