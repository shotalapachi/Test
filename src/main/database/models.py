from sqlalchemy import Column, Integer, String
from .database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    location = Column(String, nullable=False)
    image = Column(String, nullable=True)
    owner = Column(String, nullable=False)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)





