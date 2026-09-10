from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Path

from category.schemas import CategorySchema, CreateCategorySchema

router = APIRouter(prefix="/categories")

@router.get('/')
async def get_all_categories() -> list[CategorySchema]:
    return []

@router.get('/{id}')
async def get_category_by_id(
    id: Annotated[int, Path(title="ID to get category")]
) -> CategorySchema | None: # TODO: remove NOne
    return

@router.get('/by-slug/{slug}')
async def get_category_by_slug(
    slug: Annotated[str, Path(title="Slug to get category")]
) -> CategorySchema | None: # TODO: remove NOne
    return

# TODO: ПОСЛЕДНИЕ МЕТОДЫ ДЛЯ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ
# TODO: ADD DTO
@router.post('/')
async def create_category(
    category: Annotated[CreateCategorySchema, Path(title="create category")]
) -> CategorySchema | None: # TODO: remove NOne
    return

# TODO: ADD DTO + NEW LOGIC
@router.post('/update/{id}')
async def update_category(
    id: Annotated[int, Path(title="ID to find category")],
    dto: Annotated[CategorySchema, Path(title="update category")] 
) -> CategorySchema | None: # TODO: remove NOne
    return 

@router.delete('/{id}')
async def delete_category(
    id: Annotated[int, Path(title="ID to delete category")]
) -> int:
    return id