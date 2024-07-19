from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.execptions import CategoryAlreadyExistsError
from app.services import category as category_service


router = APIRouter()


@router.post("/add_category", response_model=schemas.Category)
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
