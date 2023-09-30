from fastapi import FastAPI, HTTPException, Depends
from .database.database import *
from sqlalchemy.orm import Session
from .database.schema import BookSchema
from .database import models
from .auth import auth
from .auth.auth import get_current_user

app = FastAPI()
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)
users = []


@app.get("/books")
async def read_api(author: str = None,
                   genre: str = None,
                   condition: str = None,
                   owner: str = None,
                   db: Session = Depends(get_db)):
    query = db.query(models.Books).all()
    print(author, genre, condition, owner)
    if author:
        query = db.query(models.Books).filter(models.Books.author == author).all()
    if genre:
        query = db.query(models.Books).filter(models.Books.genre == genre).all()
    if condition:
        query = db.query(models.Books).filter(models.Books.condition == condition).all()
    if owner:
        query = db.query(models.Books).filter(models.Books.owner == owner).all()

    return query


@app.post("/books")
async def create_book(book: BookSchema, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        book_model = models.Books()
        book_model.title = book.title
        book_model.author = book.author
        book_model.genre = book.genre
        book_model.description = book.description
        book_model.condition = book.condition
        book_model.location = book.location
        book_model.image = book.image
        book_model.owner = user['username']

        db.add(book_model)
        db.commit()
        db.refresh(book_model)
        return f"Book added successfully"
    except Exception as e:
        return f"Something went wrong, Try again later \n Error {e}"


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    try:
        book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

        if book_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"Book with ID {book_id} does not exist"
            )

        book_model.title = book.title
        book_model.author = book.author
        book_model.genre = book.genre
        book_model.description = book.description
        book_model.condition = book.condition
        book_model.location = book.location
        book_model.image = book.image

        db.commit()
        db.refresh(book_model)
        return f"Book successfully updated ID: {book_id}"
    except Exception as e:
        return f"Ooops something went wrong \n Error: {e} "


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

        if book_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"ID {book_id} : Does not exist"
            )

        db.query(models.Books).filter(models.Books.id == book_id).delete()

        db.commit()
        return "Book deleted successfully"
    except Exception as e:
        return f"Oops Error: {e}"
