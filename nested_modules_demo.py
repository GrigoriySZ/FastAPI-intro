from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

# uvicorn nested_modules_demo:app --reload --host 127.0.0.1 --port 8000

app = FastAPI(
    title='Pydentic демонтрация'
)

class Author(BaseModel):
    name: str = Field(..., min_length=2, max_length=100,
                      description='Имя автора')
    birth_date: Optional[int] = Field(None, description='Год рождения',
                                      ge=1000, le=2026)

class Book(BaseModel):
    title: str = Field(..., description='Название книги', examples=["Война и мир"])
    author: Author = Field(..., description='Автор книги')
    pages: Optional[int] = Field(None, description='Количество страниц')


books_db: list[Book] = []

@app.post('/books', response_model=Book, status_code=201)
async def create_book(book: Book): 
    books_db.append(book)
    return book

@app.get('/books', response_model=list[Book])
async def get_books():
    return books_db

