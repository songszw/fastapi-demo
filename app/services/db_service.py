from fastapi import HTTPException
from sqlalchemy.orm import Session


def save_to_db(db: Session, instance):
    try:
        db.add(instance)
        db.commit()
        db.refresh(instance)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return instance
