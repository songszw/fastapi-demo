from fastapi import APIRouter

from app.api.v1 import user
from app.api.v1 import category

api_router = APIRouter()

api_router.include_router(user.router, prefix="/api/v1/user", tags=["Users"])
api_router.include_router(category.router, prefix='/api/v1/category', tags=["Category"])
