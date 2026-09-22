from turtle import update
from db import PrimaryKey, SessionDep
from fastapi import APIRouter, HTTPException
from flowers.model import Flower
from flowers.schemas import FlowerCreateSchema, FlowerSchema
from flowers.service import (
    create,
    get_all,
    update,
    delete
)

router = APIRouter()

@router.get("", response_model=list[FlowerSchema])
async def getAll(session: SessionDep):
    return await get_all(session=session)

@router.post("", response_model=FlowerSchema)
async def createFlower(
    session: SessionDep,
    flower_in: FlowerCreateSchema
):
    return await create(session=session, flower_in=flower_in)

@router.post("/update")
async def updateFlower(
    session: SessionDep,
    id: PrimaryKey,
    flower_in: FlowerCreateSchema,
):
    flower = await session.get(Flower, id)

    if not flower:
        raise HTTPException(
            status_code=404,
            detail={"msg": 'Не найден'}
        )
    
    return await update(session=session, flower=flower, flower_in=flower_in)

@router.delete("")
async def deleteFlower(
    session: SessionDep,
    id: PrimaryKey
):
    return await delete(session=session, id=id)
