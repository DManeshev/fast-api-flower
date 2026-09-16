from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


if TYPE_CHECKING:
    from src.product.model import Product


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    order: Mapped[int]

    parentId: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )

    subcategories: Mapped[list["Category"]] = relationship(
        "Category",
        order_by="Category.order.desc()",
        lazy='selectin'
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        order_by="Product.createdAt"
    )
