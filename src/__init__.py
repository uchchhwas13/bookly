from fastapi import FastAPI
from src.middleware import register_middleware
from .routes.book_routes import book_router
from .routes.auth_routes import auth_router
from .routes.review_routes import review_router

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version
)

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(
    review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
