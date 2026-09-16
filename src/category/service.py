from category.model import Category
from category.schemas import CategoryCreateSchema, CategoryUpdateSchema
from db import PrimaryKey, SessionDep
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from slugify import slugify

async def get_all(*, session: SessionDep) -> list[Category]:
    result = await session.execute((
        select(Category)
        .options(selectinload(Category.subcategories))
    ))

    return list[Category](result.scalars().all())


async def get_by_id(
    session: SessionDep,
    category_id: PrimaryKey
) -> Category | None:
    query = (
        select(Category)
        .options(selectinload(Category.subcategories))
        .filter_by(id=category_id)
    )

    categories = await session.execute(query)

    category = categories.unique().scalars().first()
    
    return category


async def get_by_slug(
    session: SessionDep,
    slug: str
) -> Category | None:
    query = (
        select(Category)
        .filter_by(slug=slug)
        .options(selectinload(Category.subcategories))
    )
    
    categories = await session.execute(query)

    category = categories.scalars().first()

    return category


async def create(
    session: SessionDep,
    category_in: CategoryCreateSchema
) -> Category:
    categories = await get_all(session=session)

    category = Category(
        **category_in.model_dump(),
        slug=slugify(category_in.name),
        order=len(categories) + 1
    )

    session.add(category)
    await session.commit()
    await session.refresh(
        category, 
        attribute_names=["subcategories", "products"]
    )

    return category


async def update(
    session: SessionDep,
    category: Category,
    category_in: CategoryUpdateSchema
) -> Category:
    category_data = category.dict()

    update_data = category_in.model_dump(exclude_unset=True)

    for field in category_data:
        if field in update_data:
            if (field == 'name'):
                setattr(category, 'slug', slugify(update_data[field]))

            setattr(category, field, update_data[field])
    
    await session.commit()
    return category


async def delete(
    session: SessionDep,
    category_id: PrimaryKey
):
    category = await session.execute(select(Category).filter(Category.id == category_id))

    await session.delete(category.scalar_one())
    await session.commit()