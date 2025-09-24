from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
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


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


app = FastAPI()


@app.get("/books", response_model=list[Book])
async def get_books():
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
