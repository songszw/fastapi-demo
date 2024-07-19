from sqlalchemy.orm import Session

from app.core.execptions import CategoryAlreadyExistsError
from app.models import Category
from app.schemas.category import CategoryBase


def create_category(db: Session, category: CategoryBase, user_id):
    if get_category_by_name(db, category.name, user_id):
        raise CategoryAlreadyExistsError()
    db_category = Category(
        name=category.name,
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category_by_name(db: Session, name: str, user_id: int):
    return db.query(Category).filter(Category.name == name, Category.user_id == user_id).first()
