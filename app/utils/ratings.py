from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel


async def update_product_rating(db: AsyncSession, product_id: int) -> None:
    """
    Обновляет рейтинг товара на основе отзывов.

    Args:
        db: AsyncSession
        product_id: int
            ID товара.

    Returns:
        None
    """
    avg_rating = await db.scalar(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active.is_(True),
        )
    )

    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(rating=float(avg_rating or 0.0))
    )
