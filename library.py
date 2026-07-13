from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title='Каталог библиотеки',
    description='RESTful API для управления каталога книг',
    version='1.0.0'
)

class Book(BaseModel): 
    title: str = Field(..., min_length=1, max_length=200, description='Название книги')
    year: int = Field(..., ge=1000, le=2026, description='Год издания')
    author: str = Field(..., min_length=1, max_length=100, description='Автор книги')
    isbn: Optional[str] = Field(None, min_length=0, max_length=20, description='ISBN книги')
    pages: Optional[int] = Field(None, qt=0, description='Количество страниц')

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    year: Optional[int] = Field(None, ge=1000, le=2026)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=0, max_length=20)
    pages: Optional[int] = Field(None, qt=0)

books_db: dict[int, Book] = {
    1: Book(title="Преступление и наказание", year=1866, author="Ф. Достоевский", pages=672),
    2: Book(title="Война и мир", year=1869, author="Л. Толстой", pages=1268)
}

next_id: int = 3

@app.get('/books', 
         response_model=List[Book],
         summary='Получить список всех книг',
         description='Возвращает список всех книг')
async def get_books(
    page: int = Query(1, ge=1, description='Номер страницы'),
    limit: int = Query(10, le=100, description='Количество книг на страницу'),
    year_from: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (от)'),
    year_to: Optional[int] = Query(None, ge=1000, le=2026, description='Год издания (до)')
):    
    all_books = list(books_db.values())
    if year_from is not None:
        all_books = [b for b in all_books if b.year >= year_from]
    if year_to is not None:
        all_books = [b for b in all_books if b.year <= year_to]
    
    start = (page - 1) * limit
    end = start + limit
    return all_books[start:end]

@app.get('/books/search',
         response_model=List[Book],
         summary='Поиск книг по автору',
         description='Возвращает списко книг, у которого автор совпадает с запросом')
async def search_books(
    author: str = Query(..., min_length=1, max_length=100, description='Имя автора книг')
):
    all_books = list(books_db.values())
    result = [b for b in all_books if author.lower() in b.author.lower()]
    if not result: 
        raise HTTPException(status_code=404, detail='Books not found')
    return result

@app.get('/books/{book_id}',
         response_model=Book,
         summary='Получить книгу по ID',
         description='Возвращает книгу с указанным идентификатором')
async def get_book(
    book_id: int = Path(..., ge=1, description='ID книги')
):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f'Book with id {book_id} not found')
    return books_db[book_id]

@app.post('/books', 
          response_model=Book,
          status_code=201,
          summary='Добавить книгу',
          description='Добавляет новый объект Book и возвращает её с присвоенным ID')
async def creacte_book(book: Book): 
    global next_id
    current_id = next_id
    next_id += 1
    books_db[current_id] = book
    return books_db[current_id]

@app.delete('/books/{book_id}',
            status_code=204,
            summary='Удалить книгу',
            description='Удаляет книгу по переданному ID')
async def delete_book(
    book_id: int = Path(..., ge=1, description='ID книги')
):
    if book_id not in books_db: 
        raise HTTPException(status_code=404, detail=f'Book with id {book_id} not found')
    del books_db[book_id]
    return