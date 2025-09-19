from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from typing import List, cast
from src.schemas import BookModel, BookUpdateModel
from src.book_data import BookDict, books


book_router = APIRouter()


@book_router.get('/', response_model=List[BookModel])
async def get_all_books():
    return books


@book_router.post('/', response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel):
    new_book = cast(BookDict, book_data.model_dump())
    books.append(new_book)
    return new_book


@book_router.get('/{book_id}', response_model=BookModel)
async def get_book(book_id: str):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")


@book_router.patch('/{book_id}', response_model=BookModel)
async def update_book(book_id: str, book_update_data: BookUpdateModel):
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")


@book_router.delete('/{book_id}', response_model=BookModel)
async def delete_book(book_id: str):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")
