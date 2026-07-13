from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

# uvicorn pydentin_demo:app --reload --host 127.0.0.1 --port 8000

app = FastAPI(
    title='Pydentic демонтрация'
)

class Book(BaseModel):
    title: str = Field(..., description='Название книги', examples=["Война и мир"])
    author: str = Field(..., description='Автор книги', examples=["Л. Толстой"])
    pages: Optional[int] = Field(None, description='Количество страниц')


books_db: list[Book] = []

@app.post('/books', response_model=Book, status_code=201)
async def create_book(book: Book): 
    books_db.append(book)
    return book

@app.get('/books', response_model=list[Book])
async def get_books():
    return books_db

