from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.services import entry as entry_service

router = APIRouter()


@router.post("/", response_model=schemas.Entry)
def create_entry(
        entry: schemas.EntryCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        print(entry)
        new_entry = entry_service.create_entry(db, entry, user_id=current_user.id)
        return new_entry
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/', response_model=schemas.EntryListResponse)
def get_entry(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        entry_list = entry_service.get_entry_list(db, user_id=current_user.id)
        total = len(entry_list)
        return {
            "total": total,
            "rows": entry_list
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/by_category', response_model=schemas.EntryListResponseByCategory)
def get_entry_by_category(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        entry_result = entry_service.get_entry_list_by_category(db, user_id=current_user.id)
        return entry_result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}",)
