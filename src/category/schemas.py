from datetime import datetime
from typing import List, Optional
from product.schemas import ProductSchema
from pydantic import BaseModel, ConfigDict, Field
from product.model import Product

class SubCategorySchema(BaseModel):
    id: int
    createdAt: datetime
    
    name: str
    slug: str
    order: int

    parentId: int | None = None

    model_config = ConfigDict(from_attributes=True)

class CategorySchema(BaseModel):
    id: int
    createdAt: datetime

    name: str
    slug: str
    order: int

    parentId: int | None = None
    subcategories: List[SubCategorySchema] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)

CategorySchema.model_rebuild()

class CategoryCreateSchema(BaseModel):
    name: str
    parentId: int | None = None

class CategoryUpdateSchema(BaseModel):
    name: str
    order: int | None = None
    parentId: int | None = None