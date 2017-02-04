from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from .meta import Base


class LibraryBook(Base):
    __tablename__ = 'library_book'
    id = Column(Integer, primary_key=True)

    owner = Column(ForeignKey('user.email'), nullable=False)
    book_info = Column(ForeignKey('market_book.id'), nullable=False)

    def __init__(self, owner, book_info_id):
        self.owner = owner
        self.book_info = book_info_id
