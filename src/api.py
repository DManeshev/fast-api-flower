from fastapi import APIRouter
from src.category.router import router as category_router

main_router = APIRouter()

main_router.include_router(
    category_router, prefix='/categories', tags=["categories"]
)