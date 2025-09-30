from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    uid: UUID

    rating: int = Field(lt=5)
    review_text: str
    user_uid: UUID | None
    book_uid: UUID | None
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str
