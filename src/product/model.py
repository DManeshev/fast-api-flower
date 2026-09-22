from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ARRAY, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.enums import BaseEnum
from src.db import Base

if TYPE_CHECKING:
    from src.category.model import Category
    from src.flowers.model import Flower

class ProductStatusEnum(BaseEnum):
    IN_STOCK = 'В наличии'
    TO_ORDER = 'Под заказ'

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    name: Mapped[str]
    slug: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(default='')
    price: Mapped[int]
    images: Mapped[list[str]] = mapped_column(ARRAY[str](String))

    isDelivery: Mapped[bool] = mapped_column(default=True)
    status: Mapped[ProductStatusEnum] = mapped_column(
        Enum(ProductStatusEnum, name="statusenum", native_enum=False, create_type=False),
        nullable=False,
    )

    categoryId: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        back_populates="products"
    )

    flowers: Mapped[list["Flower"]] = relationship(
        back_populates="products",
        secondary="product_flowers"
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, price={self.price}, images={self.images})"

    # TODO
    # orderItems    OrderItem[]

class ProductFlowers(Base):
    __tablename__ = 'product_flowers'

    productId: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True
    )

    flowerId: Mapped[int] = mapped_column(
        ForeignKey("flowers.id", ondelete="CASCADE"),
        primary_key=True
    )
