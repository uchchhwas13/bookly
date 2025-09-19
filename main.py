from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import Optional, Union, List, TypedDict, cast
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Hello world"}


@app.get('/greet')
async def greet_name(name: Optional[str] = "john doe", age: int = 0) -> dict[str, Union[str, int]]:
    return {"message": f"Hello {name}", "age": age}


class BookModel(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    publisher: str
    page_count: int


class BookDict(TypedDict):
    id: str
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


books: List[BookDict] = [
    {
        "id": "1",
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English"
    },
    {
        "id": "2",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-11",
        "page_count": 464,
        "language": "English"
    },
    {
        "id": "3",
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley",
        "published_date": "1999-10-30",
        "page_count": 352,
        "language": "English"
    },
    {
        "id": "4",
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "publisher": "MIT Press",
        "published_date": "2009-07-31",
        "page_count": 1312,
        "language": "English"
    },
    {
        "id": "5",
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "publisher": "No Starch Press",
        "published_date": "2019-05-03",
        "page_count": 544,
        "language": "English"
    }
]


@app.get('/books', response_model=List[BookModel])
async def get_all_books():
    return books


@app.post('/books', response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel):
    new_book = cast(BookDict, book_data.model_dump())
    books.append(new_book)
    return new_book


@app.get('/books/{book_id}', response_model=BookModel)
async def get_book(book_id: str):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")


@app.patch('/books/{book_id}', response_model=BookModel)
async def update_book(book_id: str, book_update_data: BookUpdateModel):
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")


@app.delete('/books/{book_id}', response_model=BookModel)
async def delete_book(book_id: str):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")
