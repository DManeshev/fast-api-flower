from fastapi import APIRouter

from src.category.router import router as category_router
from src.product.router import router as product_router
from src.yandexfiles.router import router as yandexS3_router
from src.flowers.router import router as flowers_router

main_router = APIRouter()

main_router.include_router(
    category_router, prefix='/categories', tags=["Categories"]
)

main_router.include_router(
    product_router, prefix="/products", tags=["Products"]
)

main_router.include_router(
    yandexS3_router, prefix="/files", tags=["Yandex S3"]
)

main_router.include_router(
    flowers_router, prefix="/flowers", tags=["Flowers"]
)