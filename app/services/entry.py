from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.execptions import CategoryNotFoundError, EntryNotFoundError
from app.models import Entry, Category
from app.schemas.entry import EntryCreate, CategoryEntry, EntryListResponseByCategory, Entry as EntrySchema, \
    EntryUpdate, EntryDelete, EntryDeleteResponse
from app.services.db_service import save_to_db


def create_entry(db: Session, entry: EntryCreate, user_id):
    db_category = db.query(Category).filter(Category.id == entry.category_id).first()
    if not db_category:
        raise CategoryNotFoundError("Category not found")

    db_entry = Entry(
        title=entry.title,
        content=entry.content,
        user_id=user_id,
        category_id=entry.category_id
    )
    return save_to_db(db, db_entry)


def get_entry_list(db: Session, user_id: int) -> List[Entry]:
    return db.query(Entry).filter(Entry.user_id == user_id, Entry.status == 1).all()


def get_entry_list_by_category(db: Session, user_id: int) -> EntryListResponseByCategory:
    results = (
        db.query(Category, Entry)
        .outerjoin(Entry, and_(Category.id == Entry.category_id, Entry.user_id == user_id))
        .filter(Category.user_id == user_id, Category.status == 1)
        .all()
    )

    category_dict = {}
    for category, entry in results:
        if category.id not in category_dict:
            category_dict[category.id] = {
                "id": category.id,
                "name": category.name,
                "entry_list": [],
            }

        if entry:
            category_dict[category.id]["entry_list"].append(
                EntrySchema(id=entry.id, title=entry.title, content=entry.content, category_id=entry.category_id)
            )

    category_result = []
    for category_id, category_data in category_dict.items():
        category_data["total"] = len(category_data["entry_list"])
        category_result.append(category_data)

    return EntryListResponseByCategory(
        code=200,
        total=len(category_result),
        rows=[CategoryEntry(**category) for category in category_result]
    )


def update_entry(db: Session, entry: EntryUpdate, user_id: int) -> Entry:
    db_entry = db.query(Entry).filter(entry.id == Entry.id, Entry.user_id == user_id).first()
    if not db_entry:
        raise EntryNotFoundError()

    db_category = db.query(Category).filter(entry.category_id == Category.id).first()
    if not db_category:
        raise CategoryNotFoundError()

    db_entry.title = entry.title
    db_entry.content = entry.content
    db_entry.category_id = entry.category_id

    return save_to_db(db, db_entry)


def delete_entry(db: Session, entry_id: int, user_id: int) -> EntryDeleteResponse:
    db_entry = db.query(Entry).filter(entry_id == Entry.id, Entry.user_id == user_id).first()
    if not db_entry:
        raise EntryNotFoundError()

    db_entry.status = 0
    save_to_db(db, db_entry)
    return EntryDeleteResponse(status=200, message="Entry delete success", id=db_entry.id)



