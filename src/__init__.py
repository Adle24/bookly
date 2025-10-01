from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.books.routes import book_router
from src.db.main import init_db
from src.errors import register_error_handlers
from src.reviews.routes import review_router


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

register_error_handlers(app)  # add this line

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
