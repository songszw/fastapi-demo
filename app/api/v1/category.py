from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.execptions import CategoryAlreadyExistsError, CategoryNotFoundError, CategoryDeleteError
from app.services import category as category_service

router = APIRouter()


@router.post("", response_model=schemas.ResponseDataModel[schemas.Category])
def create_category(
        category: schemas.CategoryCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        new_category = category_service.create_category(db, category, user_id=current_user.id)
        return schemas.ResponseDataModel(code=200, data=new_category, message='success')
        # return new_category
    except CategoryAlreadyExistsError as e:
        return schemas.ResponseDataModel(code=20001, message=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. ${e}")
        # raise HTTPException(status_code=400, detail=str(e))


@router.put("", response_model=schemas.ResponseDataModel[schemas.Category])
def update_category(
    category: schemas.CategoryUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    try:
        new_category = category_service.update_category(db, category, user_id=current_user.id)
        # return new_category
        return schemas.ResponseDataModel(code=200, data=new_category, message='success')
    except CategoryNotFoundError as e:
        return schemas.ResponseDataModel(code=21003, message=str(e))
        # raise HTTPException(status_code=404, detail=str(e))
    except CategoryAlreadyExistsError as e:
        return schemas.ResponseDataModel(code=21001, message=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. ${e}")
        # raise HTTPException(status_code=400, detail=str(e))


@router.get('', response_model=schemas.ResponseListModel[schemas.Category])
def get_categories(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        category_list = category_service.get_categories(db, user_id=current_user.id)
        return schemas.ResponseListModel(code=200, rows=category_list, total=len(category_list))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error{e}")


@router.delete('/{category_id}', response_model=schemas.ResponseDeleteModel[schemas.Category])
def delete_category(
        category_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = category_service.delete_category(db, category_id, user_id=current_user.id)
        return schemas.ResponseDeleteModel(code=200, message='success', id=result.id)
        # return result
    except CategoryDeleteError as e:
        return schemas.ResponseDeleteModel(code=21004, message=str(e), id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error{e}")


@router.get('/{category_id}', response_model=schemas.ResponseDataModel[schemas.Category])
def get_category_by_id(
        category_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = category_service.get_category_by_id(db, category_id, user_id=current_user.id)
        return schemas.ResponseDataModel(code=200, data=result, message='success')
    except CategoryNotFoundError as e:
        return schemas.ResponseDataModel(code=21003, message=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,  detail=f"Internal server error, {e}")

