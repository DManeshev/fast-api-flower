

from pydantic import BaseModel

class FlowerSchema(BaseModel):
    id: int
    name: str

class FlowerCreateSchema(BaseModel):
    name: str