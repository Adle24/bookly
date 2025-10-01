from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.books.routes import book_router
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tags.routes import tags_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


version = "v1"
app = FastAPI(
    version=version,
    title="Bookly",
    description="Bookly REST API for book review web service",
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
