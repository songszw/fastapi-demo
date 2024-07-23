from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.execptions import CategoryAlreadyExistsError, CategoryNotFoundError
from app.services import category as category_service

router = APIRouter()


@router.post("/", response_model=schemas.Category)
def create_category(
        category: schemas.CategoryCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        new_category = category_service.create_category(db, category, user_id=current_user.id)
        return new_category
    except CategoryAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/", response_model=schemas.Category)
def update_category(
    category: schemas.CategoryUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    try:
        new_category = category_service.update_category(db, category, user_id=current_user.id)
        return new_category
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CategoryAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=List[schemas.Category])
def get_categories(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        category_list = category_service.get_categories(db, user_id=current_user.id)
        return category_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{category_id}', response_model=schemas.Category)
def delete_category(
        category_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = category_service.delete_category(db, category_id, user_id=current_user.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
