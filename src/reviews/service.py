from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.books.service import BookService
from src.db.models import Reviews
from src.reviews.schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()


class ReviewsService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)
            review_data_dict = review_data.model_dump()
            new_review = Reviews(**review_data_dict)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
                )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            return new_review
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong {e}",
            )

    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Reviews).where(Reviews.uid == review_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Reviews).order_by(desc(Reviews.created_at))
        result = await session.exec(statement)
        return result.all()

    async def delete_review_to_from_book(
        self, review_uid: str, user_email: str, session: AsyncSession
    ):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review or (review.user is not user):
            raise HTTPException(
                detail="Cannot delete this review",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        session.add(review)

        await session.commit()
