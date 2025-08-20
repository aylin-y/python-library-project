# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from library import Library
import asyncio

app = FastAPI(title="Library API", version="1.0")

library = Library()  # shared instance


# ----- Pydantic models -----
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNRequest(BaseModel):
    isbn: str


# ----- Endpoints -----
@app.get("/books", response_model=List[BookModel])
def get_books():
    return [b.to_dict() for b in library.list_books()]


@app.post("/books", response_model=BookModel)
async def add_book(req: ISBNRequest):
    success = await library.add_book_by_isbn(req.isbn)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    book = library.find_book(req.isbn)
    return book.to_dict()


@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    removed = library.remove_book(isbn)
    if not removed:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book removed"}
