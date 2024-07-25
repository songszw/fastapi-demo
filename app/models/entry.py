from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel


class Entry(BaseModel):
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True, index=True, comment="词条id")
    title = Column(String(50), comment="词条title")
    content = Column(String(200), comment="词条内容")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment="词条所属用户id")
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False, comment="词条所属类目id")
    status = Column(Integer, default=1, nullable=False, comment="是否启用， 1启用， 0禁用")

    user = relationship("User", back_populates="entries")
    category = relationship("Category", back_populates="entries")
