from db import PrimaryKey, SessionDep
from flowers.model import Flower
from flowers.service import (get_by_ids as get_flowers_by_ids)
from product.model import Product
from product.schemas import ProductCreateSchema
from sqlalchemy import select
from slugify import slugify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

async def get_all(session: SessionDep) -> list[Product]:
    products = await session.execute((
        select(Product)
        .options(selectinload(Product.flowers))
    ))

    return list[Product](products.scalars().all())

async def get_by_category(
    session: SessionDep,
    category_slug: str
) -> list[Product]:
    products = await session.execute((
        select(Product)
        .filter(Product.category.has(slug=category_slug))
        .options(selectinload(Product.flowers))
    ))

    return list[Product](products.scalars().all())

async def by_id(
    session: SessionDep,
    product_id: PrimaryKey
) -> Product | None:
    product = await session.execute((
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.flowers))
    ))

    return product.scalars().first()

async def by_slug(
    session: SessionDep,
    slug: str
) -> Product | None:
    product = await session.execute((
        select(Product)
        .where(Product.slug == slug)
        .options(selectinload(Product.flowers))
    ))

    return product.scalars().first()

async def create(
    session: SessionDep,
    product_in: ProductCreateSchema
) -> Product:
    flowers_ids = set[int](product_in.flowers)

    flowers = []

    if flowers_ids:
        flowers = await get_flowers_by_ids(session=session, ids=flowers_ids)
        
    product: Product = Product(
        **product_in.model_dump(exclude_unset=True, exclude={'flowers'}),
        slug=slugify(product_in.name),
        flowers=flowers
    )

    try:
        session.add(product)
        
        await session.commit()
        await session.refresh(
            product,
            attribute_names=["flowers"]
        )

        return product
    except SQLAlchemyError as error:
        await session.rollback()
        raise error

async def update(
    session: SessionDep,
    product: Product,
    product_in: ProductCreateSchema,
) -> Product:
    values = product_in.model_dump(
        exclude_unset=True,
        exclude={'flowers'}
    )

    for key, value in values.items():
        if key == 'name':
            setattr(product, 'slug', slugify(value))

        setattr(product, key, value)

    if 'flowers' in product_in.model_dump() and product_in.flowers:
        flowers_ids = set[int](product_in.flowers)
        list_flowers = await get_flowers_by_ids(session=session, ids=flowers_ids)

        product.flowers = list[Flower](list_flowers)

    try:
        await session.commit()

        await session.refresh(
            product,
            attribute_names=["flowers"]
        )

        return product
    except SQLAlchemyError as error:
        print(error)
        raise error


async def delete(
    session: SessionDep,
    product_id: PrimaryKey
):
    product = await by_id(session=session, product_id=product_id)

    await session.delete(product)
    await session.commit()
 