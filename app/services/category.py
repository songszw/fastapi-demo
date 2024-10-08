from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app import schemas
from app.core.execptions import CategoryAlreadyExistsError, CategoryNotFoundError, CategoryDeleteError
from app.models import Category, Entry
from app.schemas.category import CategoryBase, CategoryUpdate, CategoryInfoResponse, CategoryDeleteResponse
from app.services.db_service import save_to_db


def create_category(db: Session, category: CategoryBase, user_id) -> schemas.Category:
    db_category = get_category_by_name(db, category.name, user_id)
    if db_category:
        if db_category.status == 0:
            db_category.status = 1
            return save_to_db(db, db_category)
        else:
            raise CategoryAlreadyExistsError()
    db_category = Category(
        name=category.name,
        user_id=user_id
    )
    return save_to_db(db, db_category)


def get_category_by_name(db: Session, name: str, user_id: int):
    return db.query(Category).filter(Category.name == name, Category.user_id == user_id).first()


def get_categories(db: Session, user_id: int) -> List[schemas.Category]:
    categories = db.query(Category).filter(Category.user_id == user_id, Category.status == 1).all()
    return [schemas.Category.from_orm(category) for category in categories]


def update_category(db: Session, category: CategoryUpdate, user_id: int) -> Category:
    db_category = db.query(Category).filter(Category.id == category.id, Category.user_id == user_id).first()
    if not db_category:
        raise CategoryNotFoundError("Category not found")

    # 判断是否已经存在相同名称的类目， 如果存在且为启用状态，则提示改category名称已存在， 如果为禁用状态则把原来的名称添加上_old_修改日期
    if category.name:
        existing_category = db.query(Category).filter(
            Category.name == category.name,
            Category.user_id == user_id,
            Category.id != category.id
        ).first()
        if existing_category:
            if existing_category.status == 1:
                raise CategoryAlreadyExistsError(f"Category with name '{category.name}' already exists.")
            else:
                existing_category.name = f"{existing_category.name}_old_{datetime.now()}"
                save_to_db(db, existing_category)

    for var, value in vars(category).items():
        setattr(db_category, var, value) if value else None

    return save_to_db(db, db_category)


def delete_category(db: Session, category_id: int, user_id: int) -> schemas.Category:
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not db_category:
        raise CategoryNotFoundError()

    entries = db.query(Entry).filter(Entry.category_id == category_id, Entry.status == 1).all()
    if entries:
        #
        # return CategoryDeleteResponse(
        #     code=21004,
        #     message='Cannot delete category with active entries',
        #     id=category_id
        # )
        raise CategoryDeleteError("Cannot delete category with active entries")

    db_category.status = 0
    return save_to_db(db, db_category)


def get_category_by_id(db: Session, category_id: int, user_id: int) -> schemas.Category:
    db_category = db.query(Category).filter(category_id == Category.id, Category.user_id == user_id).first()
    if not db_category:
        raise CategoryNotFoundError()

    return db_category
