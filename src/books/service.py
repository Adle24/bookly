from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book: BookCreateModel, user_uid, session: AsyncSession):
        data_dict = book.model_dump()
        new_book = Book(**data_dict)
        new_book.user_uid = user_uid
        session.add(new_book)

        await session.commit()
        return new_book

    async def update_book(
        self, book_id: str, book: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_id, session)

        if book_to_update is not None:
            data_dict = book.model_dump()

            for key, value in data_dict.items():
                setattr(book_to_update, key, value)

            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_id, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
        else:
            return None
