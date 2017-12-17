from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy import Integer

from .meta import Base


class BookRating(Base):
    __tablename__ = 'book_rating'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Text, ForeignKey('user.email'))
    book_id = Column(Integer, ForeignKey('book.id'))
    value = Column(Integer)

    def __init__(self, user_id, book_id, value):
        self.user_id = user_id
        self.book_id = book_id,
        self.value = value
