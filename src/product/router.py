

from db import PrimaryKey, SessionDep
from fastapi import APIRouter, HTTPException
from product.schemas import ProductCreateSchema, ProductSchema
from product.service import by_id, by_slug, create, delete, get_all, get_by_category, update

router = APIRouter()

@router.get("", response_model=list[ProductSchema])
async def get_all_products(session: SessionDep):
    """ Get ALL Products """
    return await get_all(session=session)

@router.get("/by-category", response_model=list[ProductSchema])
async def get_products_by_categories(
    session: SessionDep,
    category_slug: str,
):
    return await get_by_category(session=session, category_slug=category_slug)

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product_by_id(
    session: SessionDep,
    product_id: PrimaryKey
):
    """ Get product by ID """
    product = await by_id(session=session, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Товар не найден'}
        )
    
    return product

@router.get("/by-slug/{slug}", response_model=ProductSchema)
async def get_product_by_slug(
    session: SessionDep,
    slug: str
):
    """ Get product by slug """
    product = await by_slug(session, slug)

    if not product:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Товар не найден'}
        )

    return product; 

# TODO: ADD AUTH
@router.post("", response_model=ProductSchema)
async def create_product(
    session: SessionDep,
    product_in: ProductCreateSchema
):
    """ Create product """
    product = await create(session=session, product_in=product_in)
    return product

# TODO: ADD AUTH 
@router.post("/update/{product_id}", response_model=ProductSchema)
async def update_product(
    session: SessionDep,
    product_id: PrimaryKey,
    product_in: ProductCreateSchema,
):
    """ Update product """
    product = await get_product_by_id(session=session, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Товар не найден'}
        )

    product = await update(session=session, product=product, product_in=product_in)
    return product

# TODO: ADD AUTH
@router.delete("/{product_id}")
async def delete_product(
    session: SessionDep,
    product_id: PrimaryKey
):
    return await delete(session=session, product_id=product_id)
