from db import PrimaryKey, SessionDep
from fastapi import HTTPException
from flowers.model import Flower
from flowers.schemas import FlowerCreateSchema
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

async def get_all(session: SessionDep):
    list_flowers = await session.scalars(select(Flower))
    return list[Flower](list_flowers.all())

async def get_by_ids(session: SessionDep, ids: set[int]):
    list_flowers = await session.scalars(
        select(Flower).where(Flower.id.in_(ids))
    )
    return list_flowers.all()

async def create(
    session: SessionDep,
    flower_in: FlowerCreateSchema
) -> Flower:
    flower = Flower(**flower_in.model_dump(exclude_unset=True))

    try:
        session.add(flower)

        await session.commit()
        await session.refresh(flower)

        return flower
    except SQLAlchemyError as error:
        await session.rollback()
        raise error

async def update(
    session: SessionDep,
    flower: Flower,
    flower_in: FlowerCreateSchema
) -> Flower | None:
    flower_dict = flower_in.model_dump(exclude_unset=True)

    try:
        setattr(flower, 'name', flower_dict.get('name'))

        await session.commit()
        await session.refresh(flower)

        return flower
    except SQLAlchemyError as error:
        await session.rollback()
        raise error

async def delete(
    session: SessionDep,
    id: PrimaryKey
):
    find_flower = await session.get(Flower, id)

    if not find_flower:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Не найден'}
        )

    await session.delete(find_flower)
    await session.commit()