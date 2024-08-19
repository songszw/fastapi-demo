from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.execptions import CategoryNotFoundError, EntryNotFoundError
from app.services import entry as entry_service

router = APIRouter()


@router.post("", response_model=schemas.ResponseDataModel[schemas.Entry])
def create_entry(
        entry: schemas.EntryCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        new_entry = entry_service.create_entry(db, entry, user_id=current_user.id)
        return schemas.ResponseDataModel(code=200, data=new_entry, message='success')
    except CategoryNotFoundError as e:
        return schemas.ResponseDataModel(code=21003, message=str(e))
        # raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error{e}")


@router.get('', response_model=schemas.ResponseListModel[schemas.Entry])
def get_entry(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        entry_list = entry_service.get_entry_list(db, user_id=current_user.id)
        total = len(entry_list)
        return schemas.ResponseListModel(code=200, rows=entry_list, total=total)
        # {
        #     "code": 200,
        #     "total": total,
        #     "rows": entry_list
        # }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/by_category', response_model=schemas.ResponseListModel[schemas.CategoryEntry])
def get_entry_by_category(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        entry_result = entry_service.get_entry_list_by_category(db, user_id=current_user.id)
        total = len(entry_result)
        print(entry_result)
        return schemas.ResponseListModel(code=200, rows=entry_result, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}",)


@router.put('', response_model=schemas.ResponseDataModel[schemas.Entry])
def update_entry(
        entry: schemas.EntryUpdate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        entry_result = entry_service.update_entry(db, entry, user_id=current_user.id)
        return schemas.ResponseDataModel(code=200, message='success', data=entry_result)
        # return entry_result
    except EntryNotFoundError as e:
        return schemas.ResponseDataModel(code=20003, message=str(e))
        # raise HTTPException(status_code=400, detail=str(e))
    except CategoryNotFoundError as e:
        return schemas.ResponseDataModel(code=21003, message=str(e))
        # raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}")


@router.delete('/{entry_id}', response_model=schemas.ResponseDeleteModel[schemas.Entry])
def delete_entry(
        entry_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = entry_service.delete_entry(db, entry_id, user_id=current_user.id)
        return schemas.ResponseDeleteModel(code=200, message="success", id=result.id)
    except EntryNotFoundError as e:
        return schemas.ResponseDeleteModel(code=20003, message=str(e), id=entry_id)
        # raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}")


@router.get('/{entry_id}', response_model=schemas.EntryInfoResponse)
def get_entry_by_id(
        entry_id: int,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
):
    try:
        result = entry_service.get_entry_by_id(db, entry_id, user_id=current_user.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error, {e}")
