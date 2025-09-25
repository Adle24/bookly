from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.books.routes import book_router
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


version = "v1"
app = FastAPI(
    version=version,
    title="Bookly",
    description="Bookly REST API for book review web service",
    lifespan=lifespan,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
