from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from .meta import Base


class LibraryBook(Base):
    __tablename__ = 'library_book'
    id = Column(Integer, primary_key=True)

    owner = Column(ForeignKey('User.id'), nullable=False)
    book_info = Column(ForeignKey('MarketBook.email'), nullable=False)
