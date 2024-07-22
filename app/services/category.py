from typing import List

from sqlalchemy.orm import Session

from app.core.execptions import CategoryAlreadyExistsError, CategoryNotFoundError
from app.models import Category
from app.schemas.category import CategoryBase, CategoryUpdate
from app.services.db_service import save_to_db


def create_category(db: Session, category: CategoryBase, user_id):
    if get_category_by_name(db, category.name, user_id):
        raise CategoryAlreadyExistsError()
    db_category = Category(
        name=category.name,
        user_id=user_id
    )
    return save_to_db(db, db_category)


def get_category_by_name(db: Session, name: str, user_id: int):
    return db.query(Category).filter(Category.name == name, Category.user_id == user_id).first()


def get_categories(db: Session, user_id: int) -> List[Category]:
    return db.query(Category).filter(Category.user_id == user_id).all()


def upload_category(db: Session, category: CategoryUpdate, user_id: int) -> Category:
    db_category = db.query(Category).filter(Category.id == category.id, Category.user_id == user_id).first()
    if not db_category:
        raise CategoryNotFoundError("Category not found")

    for var, value in vars(category).items():
        setattr(db_category, var, value) if value else None

    return save_to_db(db, db_category)
