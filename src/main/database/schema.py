from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    description: str
    condition: str
    location: str
    image: str
    owner: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Godfather",
                "author": "Mario Puzo",
                "genre": "Thriller",
                "description": "Vito Corleone's life",
                "condition": "New",
                "location": "Tbilisi",
                "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1347688426i/4858791.jpg",
                "owner": "Nika_Alaverdashvili"
            }
        }
