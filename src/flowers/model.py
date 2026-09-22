from typing import TYPE_CHECKING
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.product.model import Product

class Flower(Base):
    __tablename__ = "flowers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="flowers",
        secondary="product_flowers"
    )