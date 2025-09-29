from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel

from src.auth import models


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    user_uid: UUID | None = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    user: Optional["models.User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"
