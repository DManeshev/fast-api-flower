from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime] = mapped_column(server_default=func.now())
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    order: Mapped[int]


# model Subcategory {
#   id         Int       @id @default(autoincrement())
#   name       String    @unique
#   slug       String    @unique
#   order      Int

#   products   Product[]
#   category   Category  @relation(fields: [categoryId], references: [id])
#   categoryId Int       @map("category_id")
# }
    

# model Category {
#   products      Product[]
#   subCategories Subcategory[]
# }