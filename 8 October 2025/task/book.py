from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Bookstore API")

# Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    in_stock: bool

# In-memory "database" using a dictionary
books_db = {
    1: Book(id=1, title="The Alchemist", author="Paulo Coelho", price=201.9, in_stock=True),
    2: Book(id=2, title="1984", author="George Orwell", price=215.3, in_stock=True),
    3: Book(id=3, title="To kill a mocking bird", author="Harpet Lee", price=212.99, in_stock=False)
}


@app.get("/")
def home():
    return {"message": "Welcome to the Bookstore"}


@app.get("/books", response_model=List[Book])
def get_books(title: Optional[str] = None,
              author: Optional[str] = None,
              min_price: Optional[float] = None,
              max_price: Optional[float] = None,
              in_stock: Optional[bool] = None):
    results = list(books_db.values())
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if min_price is not None:
        results = [book for book in results if book.price >= min_price]
    if max_price is not None:
        results = [book for book in results if book.price <= max_price]
    if in_stock is not None:
        results = [book for book in results if book.in_stock == in_stock]
    return results


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id in books_db:
        return books_db[book_id]
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=Book)
def add_book(book: Book):
    if book.id in books_db:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books_db[book.id] = book
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    if book_id in books_db:
        books_db[book_id] = updated_book
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id in books_db:
        deleted_book = books_db.pop(book_id)
        return {"message": f"Deleted book '{deleted_book.title}' successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
