from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Author

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
async def get_authors(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=schemas.Author)
async def create_author(
    author: schemas.AuthorCreate, db: Annotated[Session, Depends(get_db)]
):
    db_author = db.scalar(select(Author).where(Author.name == author.name))
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
async def get_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud.get_author_by_id(db, author_id)


@app.get("/books/", response_model=list[schemas.Book])
async def get_books(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_books(db)


@app.post("/books/", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate, db: Annotated[Session, Depends(get_db)]
):
    return crud.create_book(db, book)


@app.get("/{author_id}/books/", response_model=list[schemas.Book])
def get_books_by_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    books = crud.get_books_by_author_id(db, author_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this author")

    return books
