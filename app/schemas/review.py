from pydantic import BaseModel, Field
from datetime import datetime


class ReviewCreate(BaseModel):
    product_id: int = Field(description="ID товара")
    comment: str | None = Field(None, max_length=500, description="Комментарий к товару")
    grade: int = Field(ge=1, le=5, description="Оценка товара (1-5)")


class Review(BaseModel):
    id: int = Field(description="Уникальный идентификатор отзыва")
    user_id: int = Field(description="ID пользователя")
    product_id: int = Field(description="ID товара")
    comment: str | None = Field(None, description="Комментарий к товару")
    comment_date: datetime = Field(description="Дата комментария")
    grade: int = Field(description="Оценка товара (1-5)")
    is_active: bool = Field(description="Активность отзыва")