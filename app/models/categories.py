from typing import Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
    
    # Обновление модели Category с самоссылающейся связью (родительская и дочерняя категории)
    parent: Mapped[Optional["Category"]] = relationship("Category",
            remote_side="Category.id",
            back_populates="children",
            )
    children: Mapped[list["Category"]] = relationship("Category",
            back_populates="parent",
            )
