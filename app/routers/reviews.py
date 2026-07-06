from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from app.utils.ratings import update_product_rating
from app.auth import get_current_buyer, get_current_admin

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.

    Args:
        db: AsyncSession
            Сессия базы данных.

    Returns:
        list[ReviewSchema]: Список активных отзывов.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active==True))
    reviews = result.all()
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: UserModel = Depends(get_current_buyer)
):
    """
    Создаёт новый отзыв для товара (только для 'buyer').

    Args:
        review: ReviewCreate
            Данные для создания отзыва.
        db: AsyncSession
            Сессия базы данных.
        current_user: UserModel
            Текущий пользователь.
    """
    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True)
    )
    if not product_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    new_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(new_review)
    await db.flush()

    # Обновляем рейтинг товара
    await update_product_rating(db, review.product_id)

    await db.commit()
    await db.refresh(new_review)
    return new_review


@router.delete("/{review_id}", response_model=ReviewSchema)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_admin),
):
    """
    Удаляет отзыв на товар (только для 'admin').

    Args:
        review_id: int
            ID отзыва.
        db: AsyncSession
            Сессия базы данных.
        current_user: UserModel
            Текущий пользователь.

    Returns:
        dict: Сообщение о удалении отзыва.
    """
    review = await db.get(ReviewModel, review_id)
    if not review or not review.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive")

    product_id = review.product_id
    await db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == review_id)
        .values(is_active=False)
    )
    await update_product_rating(db, product_id)
    await db.commit()
    return {"message": "Review deleted"}