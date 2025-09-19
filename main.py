from fastapi import FastAPI
from typing import Optional, Union

from pydantic import BaseModel

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Hello world"}


@app.get('/greet')
async def greet_name(name: Optional[str] = "john doe", age: int = 0) -> dict[str, Union[str, int]]:
    return {"message": f"Hello {name}", "age": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post('/create_book')
async def create_book(book_data: BookCreateModel) -> dict[str, str]:
    return {
        "title": book_data.title,
        "author": book_data.author
    }


@app.get('/book/{book_id}')
async def get_book(book_id: str) -> dict[str, str]:
    return {"": ""}


@app.put('/book/{book_id}')
async def update_book(book_id: str) -> dict[str, str]:
    return {"": ""}


@app.delete('/book/{book_id}')
async def delete_book(book_id: str) -> dict[str, str]:
    return {"": ""}
