from pydantic import BaseModel


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
