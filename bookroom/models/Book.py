from sqlalchemy import Column, String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

# from .Review import Review
from .meta import Base


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    author = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    description = Column(String)
    image = Column(String)

    def __init__(self, name, author, year, genre, description, image):
        self.name = name
        self.author = author
        self.year = year
        self.genre = genre
        self.description = description
        self.image = image
