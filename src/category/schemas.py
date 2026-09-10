from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    createdAt: datetime
    name: str
    slug: str
    order: int

class CreateCategorySchema(BaseModel):
    name: str
    order: Optional[int] = None
    subCategories: Optional[List] # TODO: subCategoryDto[]
