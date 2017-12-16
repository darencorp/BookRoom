from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from .meta import Base


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    body = Column(Text)
    _date = Column(DateTime)
    modified = Column(Boolean)

    def __init__(self, user_id, book_id, body, date, modified=False):
        self.user_id = user_id
        self.book_id = book_id,
        self.body = body,
        self._date = date,
        self.modified = modified
