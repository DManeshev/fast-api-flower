from datetime import datetime
from typing import Optional
from flowers.schemas import FlowerSchema
from product.model import ProductStatusEnum
from pydantic import BaseModel, ConfigDict

class ProductSchema(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime

    name: str
    slug: str
    description: Optional[str] = ''
    price: int
    images: list[str]

    isDelivery: bool
    status: ProductStatusEnum

    categoryId: int
    flowers: list[FlowerSchema]

    model_config = ConfigDict(from_attributes=True)

class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] | None = ''
    price: int
    images: list[str]

    isDelivery: bool
    status: Optional[ProductStatusEnum] | None = ProductStatusEnum.IN_STOCK
    categoryId: int

    # TODO: flowers: