from fastapi import APIRouter

from app.api.v1 import user
from app.api.v1 import category
from app.api.v1 import entry

api_router = APIRouter()

api_router.include_router(user.router, prefix="/api/v1/user", tags=["Users"])
api_router.include_router(category.router, prefix='/api/v1/category', tags=["Category"])
api_router.include_router(entry.router, prefix='/api/v1/entry', tags=["Entry"])
