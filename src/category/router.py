from src.db import PrimaryKey, SessionDep
from fastapi import APIRouter, HTTPException
from slugify import slugify

from category.schemas import (
    CategorySchema,
    CategoryUpdateSchema,
    CategoryCreateSchema,
    SubCategorySchema
)

from category.service import (
    delete,
    get_all,
    get_by_id,
    get_by_slug,
    create,
    update,
)

router = APIRouter()


@router.get("", response_model=list[CategorySchema])
async def get_all_categories(session: SessionDep):
    """ Return all categories """
    return await get_all(session=session)

    
@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: PrimaryKey, session: SessionDep):
    """ Return category by ID """
    category = await get_by_id(session=session, category_id=category_id)
    
    if not category:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Категория не найдена'}
        )

    return category


@router.get("/by-slug/{category_slug}", response_model=CategorySchema)
async def get_category_by_slug(
    category_slug: str,
    session: SessionDep
):
    """ Return category by SLUG """
    category = await get_by_slug(session=session, slug=category_slug)

    if not category:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Категория не найдена'}
        )
    
    return category


# TODO: ПОСЛЕДНИЕ ТРИ МЕТОДА ДЛЯ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ
@router.post("", response_model=CategorySchema)
async def create_category(
    category_in: CategoryCreateSchema,
    session: SessionDep
):
    """ Create category """
    slug: str = slugify(category_in.name)
    
    existCategory = await get_by_slug(session=session, slug=slug)

    if existCategory:
        raise HTTPException(
            status_code=400,
            detail={"msg": "Категория с таким именем уже добавлена"}
        )

    category = await create(session=session, category_in=category_in)
    return category


@router.post('/update/{category_id}', response_model=CategorySchema)
async def update_category(
    session: SessionDep,
    category_id: PrimaryKey,
    category_in: CategoryUpdateSchema,
):
    """ Update category """
    category = await get_by_id(session=session, category_id=category_id)
    
    if not category:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Категория не найдена'}
        )
    
    category = await update(session=session, category=category, category_in=category_in)
    return category

@router.delete('/{category_id}', response_model=None)
async def delete_category(
    session: SessionDep,
    category_id: PrimaryKey
):
    """ Delete category """
    category = await get_by_id(session=session, category_id=category_id)
    
    if not category:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Категория не найдена'}
        )
    
    await delete(session=session, category_id=category_id)