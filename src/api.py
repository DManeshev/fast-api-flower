from fastapi import APIRouter

from src.category.router import router as category_router
from src.product.router import router as product_router

main_router = APIRouter()

main_router.include_router(
    category_router, prefix='/categories', tags=["Categories"]
)

main_router.include_router(
    product_router, prefix="/products", tags=["Products"]
)