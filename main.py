from fastapi import FastAPI
from pydantic import BaseModel

books = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "Askar Adilet",
        "publisher": "O'Rielly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Fluent Python",
        "author": "Lucian Ramalho",
        "publisher": "O'Rielly Media",
        "published_date": "2024-04-01",
        "page_count": 890,
        "language": "English",
    },
    {
        "id": 3,
        "title": "Learning Python",
        "author": "Mark Lutz",
        "publisher": "O'Rielly Media",
        "published_date": "2025-02-01",
        "page_count": 1520,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Introducing Python",
        "author": "Bill Lubanovic",
        "publisher": "O'Rielly Media",
        "published_date": "2025-09-01",
        "page_count": 645,
        "language": "English",
    },
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


app = FastAPI()


@app.get("/books", response_model=Book)
async def get_books():
    return books


@app.post("/books")
async def create_book() -> dict:
    pass


@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    pass


@app.patch("/book/{book_id}")
async def update_book(book_id: int) -> dict:
    pass


@app.delete("/book/{book_id}")
async def delete_book(book_id: int) -> dict:
    pass
