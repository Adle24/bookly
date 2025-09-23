from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet_name(age: int, name: str | None = "User") -> dict[str, str]:
    return {"message": f"Hello, {name}. You are {age} years old."}


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author,
    }


@app.get("/get_headers")
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {
        "Accept": accept,
        "Content-Type": content_type,
        "User-Agent": user_agent,
        "Host": host,
    }

    return request_headers
