from db import PrimaryKey, SessionDep
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
    product: Product = Product(
        **product_in.model_dump(exclude_unset=True),
        slug=slugify(product_in.name)
    )

    try:
        session.add(product)
        
        await session.commit()
        await session.refresh(product)

        return product
    except SQLAlchemyError as error:
        await session.rollback()
        raise error

async def update(
    session: SessionDep,
    product: Product,
    product_in: ProductCreateSchema,
) -> Product:
    product_dict = product_in.model_dump(exclude_unset=True)

    try:
        for key, value in product_dict.items():
            if key == 'name':
                setattr(product, 'slug', slugify(value))

            setattr(product, key, value)

        await session.commit()
        await session.refresh(product)

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
 